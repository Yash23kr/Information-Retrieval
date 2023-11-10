
from nltk.corpus import stopwords
import sys
with open(str(sys.argv[2]), "r") as f:
    query_ranks = f.read()

# store the list of documents for every query in a dictionary
query_ranks = query_ranks.split("\n") 
query_ranks = [query_result.split(" ") for query_result in query_ranks]
query_ranks = query_ranks[:-1]
#Create a dictionary of query ids and doc ids in int form
#Convert the list of strings to list of ints
# query_ranks = {int(query_result[0]): [int(doc_id) for doc_id in query_result[1:]] for query_result in query_ranks}
query_ranks = {query_result[0]: [doc_id for doc_id in query_result[1:]] for query_result in query_ranks}
# remove the first(":") and last element(" ") of every list in the dictionary
for key in query_ranks:
    query_ranks[key] = query_ranks[key][1:-1]

for key in query_ranks:
    query_ranks[key] = query_ranks[key][:20]

# print(query_ranks)

# from cranquel file, create a dictionary with query ids(first number of each line) as keys and a dictionary as value

def get_query_ids():            #returns a dictionary with query ids as keys and query numbers as values
    query_ids={}
    with open(str(sys.argv[2]), "r") as f:      #sys.argv[2] is the cranqrel file
        content = f.readlines()
    for i in range(len(content)):       #i is the line number
        query_ids[i+1]=(int)(content[i].split()[0])     #query_ids[i+1] is the query number
    return query_ids

query_ids=get_query_ids()
# print (query_ids)
    

def get_rel_docs():                     #returns a dictionary with query ids as keys and a dictionary as value
    with open(str(sys.argv[1]), "r") as f:      #sys.argv[1] is the cranqrel file
        content = f.readlines()            #content is a list of strings
    content = [x.strip() for x in content]      #content is a list of strings
    rel_docs = {}
    for i in range(len(content)):
        content[i] = content[i].split()
        # print (content[i][0],content[i][1],content[i][2])
        if query_ids[(int)(content[i][0])] not in rel_docs:
            rel_docs[query_ids[(int)(content[i][0])]] = {}
        rel_docs[query_ids[(int)(content[i][0])]][(int)(content[i][1])] = max(0,(int)(content[i][2]))
    return rel_docs
# print (get_rel_docs())

def get_prec_at_k(query_ranks, rel_docs, k):        #k=10 or 20
    prec_at_k = {}
    for key in query_ranks:     #key is query id
        prec_at_k[key] = 0
        rel_doc = 0
        sum=0
        for i in range(k):
            if (int)(query_ranks[key][i]) in rel_docs[(int)(key)]:
                rel_doc += 1
            sum+=rel_doc/(i+1)
        prec_at_k[key] = sum/k

    return prec_at_k

prec_at_10 = get_prec_at_k(query_ranks, get_rel_docs(), 10)     #prec_at_10 is a dictionary
prec_at_20 = get_prec_at_k(query_ranks, get_rel_docs(), 20)     #prec_at_20 is a dictionary

def get_avg_prec_at_k(query_ranks, rel_docs, k):        #k=10 or 20
    avg_prec_at_k = 0
    prec_at_k = get_prec_at_k(query_ranks, rel_docs, k)     #prec_at_k is a dictionary
    for key in prec_at_k:
        avg_prec_at_k += prec_at_k[key]     

    avg_prec_at_k = avg_prec_at_k/len(prec_at_k)        #len(prec_at_k) is the number of queries

    return avg_prec_at_k

avg_prec_at_10 = get_avg_prec_at_k(query_ranks, get_rel_docs(), 10)     
avg_prec_at_20 = get_avg_prec_at_k(query_ranks, get_rel_docs(), 20)

import math
def get_ndcg(query_ranks, rel_docs, k):     #k=10 or 20
    dcg={}
    ndcg={}
    for key in query_ranks:     #key is query id
        dcg[key]=0
        for i in range(k):      #i is the rank of the doc
            if i==0:
                if (int)(query_ranks[key][i]) in rel_docs[(int)(key)]:
                    dcg[key]+=rel_docs[(int)(key)][(int)(query_ranks[key][i])]
            elif (int)(query_ranks[key][i]) in rel_docs[(int)(key)]:
                dcg[key]+=rel_docs[(int)(key)][(int)(query_ranks[key][i])]/math.log(i+2,2)

    
        sorted_rel_docs=sorted(rel_docs[(int)(key)].values(),reverse=True)      #sorted_rel_docs is a list of relevance scores of all docs for a particular query
        sum=0
        # print(sorted_rel_docs)
        for i in range(len(sorted_rel_docs)):       #i is the rank of the doc
            if sorted_rel_docs[i]<=0:
                break
            if i==0:
                sum+=sorted_rel_docs[i]
            else:
                sum+=sorted_rel_docs[i]/math.log(i+2,2)     #i+2 because i starts from 0
        if(sum==0):
            ndcg[key]=0
        else:
            ndcg[key]=dcg[key]/sum      #dcg[key] is the dcg value for a particular query
    return ndcg

ndcg_at_10=get_ndcg(query_ranks, get_rel_docs(), 10)        #ndcg_at_10 is a dictionary    
ndcg_at_20=get_ndcg(query_ranks, get_rel_docs(), 20)        #ndcg_at_20 is a dictionary    

def get_avg_ndcg(query_ranks, rel_docs, k):     #k=10 or 20
    avg_ndcg=0
    ndcg=get_ndcg(query_ranks, rel_docs, k)     #ndcg is a dictionary
    for key in ndcg:
        avg_ndcg+=ndcg[key]
    avg_ndcg=avg_ndcg/len(ndcg)     #len(ndcg) is the number of queries
    return avg_ndcg


avg_ndcg_10=get_avg_ndcg(query_ranks, get_rel_docs(), 10)
avg_ndcg_20=get_avg_ndcg(query_ranks, get_rel_docs(), 20)
        
def save_to_file(filename):     #filename is a string
    with open(filename,"w") as f:       #filename is a string
        f.write("Precision@10:\n")          
        for key in query_ranks:
            f.write("\n"+key+"\t"+str(prec_at_10[key]))     #prec_at_10[key] is a float
        f.write("\n\nPrecision@20:\n")
        for key in query_ranks:
            f.write("\n"+key+"\t"+str(prec_at_20[key]))     #prec_at_20[key] is a float
        f.write("\n\nNDCG@10:\n")
        for key in query_ranks:
            f.write("\n"+key+"\t"+str(ndcg_at_10[key]))     #ndcg_at_10[key] is a float
        f.write("\n\nNDCG@20:\n")
        for key in query_ranks:
            f.write("\n"+key+"\t"+str(ndcg_at_20[key]))     #ndcg_at_20[key] is a float

        f.write("\n\nAverage Precision@10: "+str(avg_prec_at_10)+"\n")      
        f.write("Average Precision@20: "+str(avg_prec_at_20)+"\n")
        f.write("Average NDCG@10: "+str(avg_ndcg_10)+"\n")
        f.write("Average NDCG@20: "+str(avg_ndcg_20)+"\n")

save_to_file("Assignment2_21CS30059_metrics"+str(sys.argv[2])[-5]+".txt")      
