import math
import re
# from google.cloud import storage
import pickle
import concurrent.futures
from inverted_index_gcp import *
from concurrent.futures import ThreadPoolExecutor
from nltk.stem.porter import *


class BackendSearch:
    def __init__(self):
        self.doc_len = None
        self.index_title = None
        self.index_body = None
        self.title_doc_len = None

    def read_pkl_from_gcs(self, bucket_name, file_name):
        # """Read a .pkl file from a Google Cloud Storage bucket."""
        # Get the bucket
        client = storage.Client()

        bucket = client.bucket(bucket_name)

        # Get the blob (file) from the bucket
        blob = bucket.blob(file_name)

        # Download the file to a local temporary file
        temp_file_path = "/tmp/temp_file.pkl"  # You can change the path as needed
        blob.download_to_filename(temp_file_path)

        # Load the data from the pickle file
        with open(temp_file_path, "rb") as f:
            data = pickle.load(f)

        return data

    # Function to calculate IDF
    def calculate_idf(self, N, DF):
        return math.log((N - DF + 0.5) / (DF + 0.5) + 1)  # Add 1 to avoid division by zero

    # Load data from inverted index
    def load_data(self, query, index):
        data = []

        # Define a function to load data for a single word in parallel
        def load_word_data(word):
            postings = index.read_a_posting_list('', word, '208899385irproject')
            return (word, postings)

        # Use ThreadPoolExecutor to run the loading tasks in parallel
        with ThreadPoolExecutor() as executor:
            # Submit tasks for each word in the query
            futures = [executor.submit(load_word_data, word) for word in query]

            # Get the results as they become available
            for future in futures:
                data.append(future.result())

        return data

    def normalize_dict(self, dictionary, k):
        # Find the minimum and maximum values in the dictionary
        min_val = min(dictionary.values())
        max_val = max(dictionary.values())

        # Normalize the values between 0 and 1
        normalized_dict = {}
        for key, value in dictionary.items():
            normalized_value = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
            normalized_dict[key] = normalized_value * k

        return normalized_dict

    def get_results_BM25(self, query_list, index, len_docs, k, k1=1.5, b=0.75):
        N = index.n
        avg_doc_len = index.avg_doc_len
        data = self.load_data(query_list, index)
        result_dict = {}

        def _calculate_score(tf, doc_len_d):
            return tf * (k1 + 1) / (tf + k1 * (1 - b + b * (doc_len_d / avg_doc_len)))

        # Define a function to calculate BM25 score for a single word
        def calculate_bm25(word, postings):
            idf = self.calculate_idf(N, len(postings))
            scores = {}
            for doc_id, tf in postings:
                doc_len_d = len_docs.get(doc_id, 1)
                score = idf * _calculate_score(tf, doc_len_d)
                scores[doc_id] = score

            return scores

        # Use ThreadPoolExecutor to run the calculations in parallel
        with ThreadPoolExecutor() as executor:
            # Submit tasks for each word in the query
            futures = {executor.submit(calculate_bm25, word, postings): word for word, postings in data}

            # Get the results as they become available
            for future in futures:
                word = futures[future]
                result_dict[word] = future.result()

        # Merge the results from different words into a single dictionary
        merged_result1 = {}
        for word, scores in result_dict.items():
            for doc_id, score in scores.items():
                if doc_id in merged_result1:
                    merged_result1[doc_id] += score
                else:
                    merged_result1[doc_id] = score

        # Sort the merged result by score and take the top k documents
        sorted_result = sorted(merged_result1.items(), key=lambda x: x[1], reverse=True)[:k]

        result_dict = {doc_id: score for doc_id, score in sorted_result}
        return result_dict

    def split_and_remove_punctuation(self, text):
        # Use regular expression to split the text into words and remove punctuation
        words = re.findall(r'\b\w+\b', text)
        return words


    def merge_dictionaries(self, title_dict, body_dict):
        # Iterate through dict2
        for doc_id, value in body_dict.items():
            # If doc_id already exists in title_dict, add the value to the existing value
            if doc_id in title_dict:
                title_dict[doc_id] = (value*0.4)+(title_dict[doc_id]*0.6)
            # If doc_id does not exist in title_dict, add it with the value from dict2
            else:
                title_dict[doc_id] = value*0.6

        return title_dict


    def final_bm25(self, body_index, title_index, user_query, doc_len, doc_len_title, pr,all_stopwords, k1=1.5, b=0.75, top_k=5):
        RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}""", re.UNICODE)
        stemmer = PorterStemmer()

        query = [token.group() for token in RE_WORD.finditer(user_query.lower())]
        query = [token for token in query if token not in all_stopwords]
        query = [stemmer.stem(token) for token in query]

        # Function to calculate BM25 scores for a given index
        def calculate_bm25_scores(index, doc_len, k1, b):
            return self.get_results_BM25(query, index, doc_len, 5000, k1, b)

        # Use ThreadPoolExecutor to run the calculations in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks for body and title calculations
            body_future = executor.submit(calculate_bm25_scores, body_index, doc_len, 1.5, 0.75)
            title_future = executor.submit(calculate_bm25_scores, title_index, doc_len_title, 1.2, 0.6)

            # Get the results
            body_result = body_future.result()
            title_result = title_future.result()
            # dictionary = body_future.result()

        dictionary = self.merge_dictionaries( title_result,body_result)
        l = [(score, key) for key, score in dictionary.items()]
        l = sorted(l, reverse=True)[:60]
                # Iterate through dict2
        for i in range(len(l)):
            doc_id = l[i][1]
            score = l[i][0]
            if doc_id in pr.keys():
                l[i] = (score * pr[doc_id],doc_id)
            else:
                l[i] = (score * 0.000085,doc_id)

        # # dictionary = self.merge_dictionaries(dictionary, title_result)
        l = sorted(l, reverse = True)[:30]

        final = [(str(doc_id), title_index.title.get(doc_id, '')) for _, doc_id in l]

        return final

