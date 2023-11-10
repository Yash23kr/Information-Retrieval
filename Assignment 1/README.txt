Name: Yash Kumar
Roll Number: 21CS30059

Information Retrieval Assignment 1: Inverted Index, Boolean Document Retrieval

Packages used:
- Python 3.10.4
- nltk 3.8.1
- spacy 3.5.3
- pickle
- sys

Installation instructions:
- Install the packages mentioned above using pip.
- Download the spacy model using the command `python -m spacy download en_core_web_sm`

Instructions to run:
- Run the command `python3 main.py <path_to_corpus> <path_to_output_file> <path_to_queries_file> <path_to_output_file>`

Dataset details:
- The corpus is a collection of 1400 documents.
- The query file contains 225 queries.
- Number of lemmatized and non stop-words in the set of documents = 6,661


Pre-processing pipeline:
- Extraction of id and text for both documents and queries.
- Tokenization using nltk's word_tokenize.
- Removal of stop words using nltk's stopwords.
- Lemmatization using spacy's en_core_web_sm model.
- Removal of single character tokens.

The document and query ids and texts are stored in a dictionary with the following structure:
- key: id
- value: text

The inverted index is stored in a dictionary with the following structure:
- key: term
- value: list of document ids in which the term occurs

The inverted index is stored in a pickle file for faster retrieval.

Boolean Retrieval Steps:
- Queries and inverted index are loaded from the text and pickle files.
- A list of document ids is generated for the first word of the query.
- For each subsequent word in the query, the list of document ids is generated and the intersection of the list of document ids is taken with the previous list of document ids.
- The list of document ids is sorted in ascending order.
- The list of document ids is written to the output file.

Output:
- The output file "Assignment1_21CS30059.txt" contains the list of document ids for each query in the following format:
    - <query_id> <comma-separated list of document ids>
- For 18 queries, the list of document ids is non-empty.
- For 207 queries, the list of document ids is empty.




