def boolean_retrieval_model(queries, inverted_index):
#     answers = {}
#     c=0
#     for query in queries:
#         id = query.split("\t")[0]
#         query_words = query.split("\t")[1].split()
#         result = set(inverted_index.get(query_words[0], []))
#         for word in query_words[1:]:
#             result.intersection_update(set(inverted_index.get(word, [])))
#             if result == set():
#                 break
#         answers[id] = list(result)
#         if list(result) != []:
#             c = c+1
            
#     print("c: ", c)
#     print ("Total queries: ", len(queries))
#     for key in answers:
#         print(key, " : ", answers[key])
#     return answers

# queries = load_queries()
# answers = boolean_retrieval_model(queries, inverted_index)
# # print(answers)
        

# # 4. Store the results in a file named: Assignment1_<ROLL_NO>_results.txt as a list of:
# # <query id> : <space separated list of document IDs>
# # Store this file in your main code directory

# def save_results(answers):
#     with open("Assignment1_21CS30059_results.txt", "w") as f:
#         for key in answers:
#             f.write(key + " : " + " ".join([str(x+1) for x in answers[key]]) + "\n")

# save_results(answers)