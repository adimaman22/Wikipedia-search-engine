# Wikipedia Search Engine
Final project of information retrieval course in data engineering BGU


## Project Overview
This project aims to develop a search engine for Wikipedia using an inverted index, BM25 ranking algorithm, and various stemming techniques.
It includes building indexes for body text and titles, optimizing query execution with multithreading, and providing a frontend for user queries.
This search engine stands out by integrating advanced data structures and algorithms to efficiently process and retrieve relevant Wikipedia articles.

## Data Overview
Our search engine is built on top of a robust dataset extracted from English Wikipedia. Here's a glimpse into the structure of the data we've worked with:
- ID: Unique identifier for each document.
- Title: The title of the Wikipedia article.
- Text: Extracted body text from the article, which may include markup and references.
- Anchor Text: Text from hyperlinks pointing to other Wikipedia articles.

![data overview](https://github.com/adimaman22/Wikipedia-search-engine/assets/162898894/0fefae00-a767-4d46-8775-28d80fb4f1d2)


## Key Features
- Inverted Index Construction: Efficient retrieval mechanism using separate indexes for body text and titles.
- Ranking with BM25: Incorporates BM25 for relevance scoring, enhancing result quality.
- Stemming and Tokenization: Utilizes Porter stemming for preprocessing, ensuring better matching.
- Multithreaded Query Execution: Speeds up query processing by running search tasks in parallel.
- Frontend Interface: Simple and interactive user interface for performing searches.

## Code Structure
The repository is organized into several key components:
- inverted_index_gcp.py: Defines the InvertedIndex class for managing the index, including methods for saving and loading index files.
- index_builder.py: Scripts for building the inverted index from the Wikipedia dataset.
- backend_search.py: Backend logic for processing queries using the inverted index and BM25.
- search_frontend.py: Frontend application for submitting search queries and displaying results.

Additional files:
- run_frontend_in_colab.ipynb: notebook showing how to run the search engine's frontend in Colab for development purposes.
- run_frontend_in_gcp.sh: command-line instructions for deploying our search engine to GCP.
- startup_script_gcp.sh: a shell script that sets up the Compute Engine instance.
- bucket_files.txt: A text file that List all index files.
- Information retrieval project report.pdf: Project report.

## Dependencies
- Flask
- NLTK
- NumPy
- pickle
- re
- ThreadPoolExecutor
- Requests
- Google Cloud Storage

## Creators
This project was created by:
- Adi Maman
- Omer Shem tov
- Guy Dulberg
