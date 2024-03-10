# Wikipedia Search Engine
Final project of information retrieval course in data engineering BGU


## Project Overview
This project aims to develop a search engine for Wikipedia using an inverted index, BM25 ranking algorithm, and various stemming techniques.
It includes building indexes for body text and titles, optimizing query execution with multithreading, and providing a frontend for user queries.
This search engine stands out by integrating advanced data structures and algorithms to efficiently process and retrieve relevant Wikipedia articles.

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

## Dependencies
- Flask
- NLTK
- NumPy
- Requests
- Google Cloud Storage

