import spacy
import string
from nltk.corpus import stopwords
import pickle
import sys

def build_dictionary_of_id_and_docs():
    with open(str(sys.argv[1])) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    docs = {}

    previd = 0
    text = ""
    for i in range (len(content)):
        if content[i].startswith(".I"):
            id = content[i].split()[1]
            docs[id] = ""
            if text != "":
                docs[previd] = text
            text = ""
            previd = id
            flag = 0

        elif content[i].startswith(".W"):
            flag=1
            text = ""
        elif flag==1:
            text = text + " " + content[i]
    
    if text != "":
        docs[previd] = text

    return docs

# docs = build_dictionary_of_id_and_docs()
# print(docs)
    

def remove_stop_words_and_punctuations_and_build_inverted_index(docs):
    nlp = spacy.load("en_core_web_sm")
    stop_words = set(stopwords.words('english'))
    inverted_index = {}
    for key in docs:
        doc = nlp(docs[key])
        for token in doc:
            if token.lemma_ == " ":
                continue
            if token.text not in stop_words and token.text not in string.punctuation:
                if token.lemma_ not in inverted_index:
                    inverted_index[token.lemma_] = [key]
                else:
                    inverted_index[token.lemma_].append(key)

    for key in inverted_index:
        inverted_index[key] = list(set(inverted_index[key]))   # remove duplicates
        inverted_index[key].sort()                       # sort
    # print (inverted_index)
    # print (len(inverted_index))
    return inverted_index

# docs=build_dictionary_of_id_and_docs()
# docs=remove_stop_words_and_punctuations_and_build_inverted_index(docs)
# print(docs)



def save_inverted_index():
    inverted_index = remove_stop_words_and_punctuations_and_build_inverted_index(build_dictionary_of_id_and_docs())
    # print (inverted_index)
    with open('model_queries_21CS30059.bin', 'wb') as f:
        pickle.dump(inverted_index, f)

save_inverted_index()