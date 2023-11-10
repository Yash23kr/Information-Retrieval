import pickle
import math
import spacy
import string
from nltk.corpus import stopwords
import sys

inverted_index = pickle.load(open(str(sys.argv[3]), "rb"))
def getDF():
    df = {}
    for term in inverted_index:
        df[term] = len(inverted_index[term])
    return df

df = getDF()

def extract_text_and_id():
    with open(str(sys.argv[2]), "r") as f:                    # open file
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

queries = remove_stop_words_and_punctuations(extract_text_and_id())



# query_scores = query_scores()
# print(scores)

#Store query scores in a txt file
# def save_scores(scores):
#     with open("query_scores_21CS30059.txt", "w") as f:
#         for query in scores:
#             f.write(query + "\n")
#             for term in scores[query]:
#                 f.write(term + " " + str(scores[query][term]) + "\n")
#             f.write("\n")

# save_scores(scores)

def build_dictionary_of_id_and_docs():
    with open(str(sys.argv[1]),"r") as f:
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

docs = build_dictionary_of_id_and_docs()

#Remove stop words and punctuations from the text
import spacy
from nltk.corpus import stopwords
import string

def remove_stop_words_and_punctuations(docs):       #Remove stop words and punctuations from the text
    nlp = spacy.load("en_core_web_sm")
    stop_words = set(stopwords.words('english'))
    new_docs = {}
    for key in docs:
        doc = nlp(docs[key])
        new_docs[key] = []
        for token in doc:
            if token.lemma_ == " ":
                continue
            if token.text not in stop_words and token.text not in string.punctuation:       #Remove stop words and punctuations
                new_docs[key].append(token.lemma_)
    
    return new_docs


#Save the dictionary in a text file
# def save_docs(docs):
#     with open("docs_21CS30059.txt", "w") as f:
#         for key in docs:
#             f.write(key + "\t")
#             for token in docs[key]:
#                 f.write(token + " ")
#             f.write("\n")

list_of_docs =remove_stop_words_and_punctuations(docs)      #Remove stop words and punctuations from the text

def get_query_vector1():    #Calculate query scores as per ltc scheme
    scores = {}

    for key in queries:
        query=queries[key]
        scores[key]={}

        for term in query:
            if term not in inverted_index:      #If term not in inverted index,
                    continue
            if term not in scores[key]:
                scores[key][term] = 1
            else:
                scores[key][term]+=1        #tf
        s=0
        for term in query:      #Calculate query scores as per ltc scheme
            if term not in inverted_index:
                    continue
            if scores[key][term]>0:
                scores[key][term] = (1+math.log(scores[key][term],10))*(math.log((1400/df[term]),10))
            else:
                scores[key][term]=0
            s+=scores[key][term]*scores[key][term]

        s=math.sqrt(s)

        for term in query:
            if term not in inverted_index:
                    continue
            if s==0:
                continue
            else:
                scores[key][term] = scores[key][term]/s

    return scores

def get_doc_vector():       #Calculate doc scores as per tf-idf scheme
    scores = {}
    c=0
    visited={}
    for key in list_of_docs:        #Calculate doc scores as per tf-idf scheme
        c+=1
        scores[c] = {}
        visited[c]={}

        doc=list_of_docs[key]       
        for token in doc:
            if token not in scores[c]:      
                scores[c][token] = 1
            else:
                scores[c][token] += 1      
        

        s=0
        
        for token in scores[c]:
            scores[c][token] = 1+math.log(scores[c][token],10)
            s+=scores[c][token]*scores[c][token]

        s=math.sqrt(s)      #normalization

        for token in scores[c]:
            scores[c][token] = scores[c][token]/s
 
    return scores


query_vector1 = get_query_vector1()
doc_vector1 = get_doc_vector()


def get_query_doc_scores():     #Calculate scores of each query and doc pair as per lnc.ltc scheme
    query_doc_scores = {}

    for key in queries:
        query_doc_scores[key] = {}
        query=queries[key]
        for c in range(1,1401):
            query_doc_scores[key][c] = 0
            for term in query:
                if term not in inverted_index:
                    continue
                if term in doc_vector1[c]:
                    # if c==486 and key=="001":
                    #     print ("486"+" "+term)
                    #     print (query_vector1[key][term], doc_vector1[c][term])
                    # if c==573 and key=="001":
                    #     print ("573"+" "+term)
                    #     print (query_vector1[key][term], doc_vector1[c][term])
                    query_doc_scores[key][c] += (query_vector1[key][term]*doc_vector1[c][term])
            
    
    #Sort in decreasing order the doc numbers according to their scores
    for key in query_doc_scores:
        query_doc_scores[key] = dict(sorted(query_doc_scores[key].items(), key=lambda item: item[1], reverse=True))
    return query_doc_scores

query_doc_scores = get_query_doc_scores()


def save_ranklist(query_doc_scores):        #save query_doc_scores in a text file
    with open("Assignment2_21CS30059_ranked_list_A.txt","w") as f:
        for key in query_doc_scores:
            f.write(key + " : ")
            c=0
            for doc in query_doc_scores[key]: 
                c+=1
                f.write(str(doc) + " ")
                if(c==50):
                    break
            f.write("\n")

save_ranklist(query_doc_scores)


def get_query_vector2():        #Calculate query scores as per Ltc scheme
    scores = {}
    for key in queries:
        query=queries[key]
        scores[key]={}
        
        for token in query:
            if token in inverted_index:
                if token not in scores[key]:
                    scores[key][token] = 1
                else:
                    scores[key][token] += 1

        s=0
        s2=0
        count=0
        for term in query:
            if term not in inverted_index:      #If term not in inverted index,
                continue
            if scores[key][term]>0:
                s2+=scores[key][term]
                count+=1

        s2=s2/count             #s2 is the average of tf of all terms in the query
        if count==0:
            den=1
        else:
            den=math.log(s2,10)+1
        for term in query:
            if term not in inverted_index:
                continue
            if scores[key][term]>0:
                scores[key][term] = (1+math.log(scores[key][term],10))/den
                scores[key][term] = scores[key][term]*math.log(1400/df[term],10)
            else:
                scores[key][term]=0
            s+=scores[key][term]*scores[key][term]

        s=math.sqrt(s)

        for term in query:
            if term not in inverted_index:
                continue
            if s==0:
                scores[key][term] = 0
            else:
                scores[key][term] = scores[key][term]/s

    return scores
query_vector2 = get_query_vector2()

def get_query_doc_scores2():        #Calculate scores of each query and doc pair as per lnc.Ltc scheme
    query_doc_scores2 = {}

    for key in queries:
        query_doc_scores2[key] = {}
        query=queries[key]
        for c in range(1,1401):
            query_doc_scores2[key][c] = 0
            for term in query:
                if term not in inverted_index:
                    continue
                if term in doc_vector1[c]:
                    query_doc_scores2[key][c] += query_vector2[key][term]*doc_vector1[c][term]
            
    
    #Sort in decreasing order the doc numbers according to their scores
    for key in query_doc_scores2:
        query_doc_scores2[key] = dict(sorted(query_doc_scores2[key].items(), key=lambda item: item[1], reverse=True))
    return query_doc_scores2

query_doc_scores2 = get_query_doc_scores2()

def save_ranklist2(query_doc_scores2):
    with open("Assignment2_21CS30059_ranked_list_B.txt","w") as f:
        for key in query_doc_scores2:
            f.write(key + " : ")
            c=0
            for doc in query_doc_scores2[key]:
                c+=1
                f.write(str(doc) + " ")
                if(c==50):
                    break
            f.write("\n")

save_ranklist2(query_doc_scores2)

def get_query_vector3():
    #Caluclate query scores as per apc scheme
    scores3 = {}
    for key in queries:
        query=queries[key]
        scores3[key]={}

        for token in query:
            if token not in inverted_index:
                    continue
            if token not in scores3[key]:
                scores3[key][token] = 1
            else:
                scores3[key][token]+=1
        
        max_tf=0
        for term in query:
            if term not in inverted_index:
                    continue
            if max_tf<scores3[key][term]:
                max_tf=scores3[key][term]

        s=0
        
        for term in query:
            if term not in inverted_index:
                    continue
            if scores3[key][term]>0:
                scores3[key][term] = (0.5+0.5*scores3[key][term]/max_tf)*max(0,math.log((1400-df[term])/df[term],10))
            else:
                scores3[key][term]=0.5
            s+=scores3[key][term]*scores3[key][term]        

        s=math.sqrt(s)
        for term in query:
            if term not in inverted_index:
                    continue
            if s==0:
                scores3[key][term] = 0
            else:
                scores3[key][term] = scores3[key][term]/s       #normalization
        
    return scores3

query_vector3 = get_query_vector3()

def get_doc_vector3():                      #Calculate doc scores as per anc scheme
    scores3 = {}
    c=0
    for key in list_of_docs:
        c+=1
        scores3[c] = {}
        doc=list_of_docs[key]               #doc is a list of tokens
        for token in doc:
            if token not in scores3[c]:
                scores3[c][token] = 1
            else:
                scores3[c][token] += 1      #tf           

        max_tf=0
        for term in doc:
            if max_tf<scores3[c][term]:
                max_tf=scores3[c][term]     #max_tf is the maximum tf of all terms in the doc
        
        s=0
        for token in scores3[c]:
            scores3[c][token] = (0.5+0.5*scores3[c][token]/max_tf)*max(0,math.log((1400-df[term])/df[term],10))
            s+=scores3[c][token]*scores3[c][token]
        
        s=math.sqrt(s)
        for token in scores3[c]:
            if s==0:
                scores3[c][token] = 0
            else:
                scores3[c][token] = scores3[c][token]/s       #normalization
        
    return scores3

doc_vector3 = get_doc_vector3()

def get_query_doc_scores3():        #Calculate scores of each query and doc pair as per anc.apc scheme
    query_doc_scores3 = {}

    for key in queries:
        query_doc_scores3[key] = {}
        query=queries[key]
        for c in range(1,1401):
            query_doc_scores3[key][c] = 0
            for term in query:
                if term not in inverted_index:
                    continue
                if term in doc_vector3[c]:
                    query_doc_scores3[key][c] += query_vector3[key][term]*doc_vector3[c][term]
    #Sort in decreasing order the doc numbers according to their scores
    for key in query_doc_scores3:
        query_doc_scores3[key] = dict(sorted(query_doc_scores3[key].items(), key=lambda item: item[1], reverse=True))
    return query_doc_scores3

query_doc_scores3 = get_query_doc_scores3()

def save_ranklist3(query_doc_scores3):
    with open("Assignment2_21CS30059_ranked_list_C.txt","w") as f:
        for key in query_doc_scores3:
            f.write(key + " : ")
            c=0
            for doc in query_doc_scores3[key]:
                c+=1
                f.write(str(doc) + " ")
                if(c==50):
                    break
            f.write("\n")

save_ranklist3(query_doc_scores3)



