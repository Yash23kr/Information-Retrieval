import spacy
import string
from nltk.corpus import stopwords
import sys


def extract_text_and_id():

    with open(str(sys.argv[1])) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    queries = {}

    previd = 0
    text = ""
    for i in range (len(content)):
        if content[i].startswith(".I"):             
            id = content[i].split()[1]                  # id of query
            queries[id] = ""                            # text of query
            if text != "":                              # if text is not empty
                queries[previd] = text                  # add text to previous id
            text = ""
            previd = id
            flag = 0

        elif content[i].startswith(".W"):               # start of text
            flag=1                                      # flag=1
            text = ""                                   # empty text
        elif flag==1:
            text = text + " " + content[i]              # add text to text
    
    if text != "":
        queries[previd] = text                          # add text to previous id

    return queries

queries = extract_text_and_id() # dictionary of id and text
# print(queries)

def remove_stop_words_and_punctuations(queries):
    nlp = spacy.load("en_core_web_sm")                  # spacy model
    stop_words = set(stopwords.words('english'))        # set of stop words
    new_queries = {}
    for key in queries:                                 
        doc = nlp(queries[key])
        new_queries[key] = []                           # list of tokens
        for token in doc:
            if token.lemma_ == " ":
                continue
            if token.text not in stop_words and token.text not in string.punctuation:
                new_queries[key].append(token.lemma_)       # list of tokens
    
    return new_queries

queries = remove_stop_words_and_punctuations(queries)      # dictionary of id and list of tokens
# print(queries)

def save_queries(queries):
    with open("queries_21CS30059.txt", "w") as f:           # save queries in a file
        for key in queries:
            f.write(key + "\t" + " ".join(queries[key]) + "\n")

save_queries(queries)
