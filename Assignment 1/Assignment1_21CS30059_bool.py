import sys
def load_queries():
    with open(str(sys.argv[2])) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content
# print(load_queries())

import pickle

def load_inverted_index():
    with open(str(sys.argv[1]), "rb") as f:
        inverted_index = pickle.load(f)
    return inverted_index

inverted_index = load_inverted_index()
# print(inverted_index)


def boolean_retrieval_model(queries, inverted_index):
    answers = {}
    # c=0
    for query in queries:
        query_id = query.split()[0]                         # id of query
        query_text = query.split()[1:]                      # text of query
        query_text = " ".join(query_text)
        query_text = query_text.lower()
        query_text = query_text.split()

        answer = set(inverted_index.get(query_text[0], [])) # answer is set of documents containing first word

        for word in query_text[1:]:
            answer = answer.intersection(set(inverted_index.get(word, []))) # intersection of answer and documents containing word
            if len(answer) == 0:
                break
        answers[query_id] = answer

        # if answer != set():
        #     c+=1
    # print ("c: ",c)
    for key in answers:
        if answers[key] == set():
            continue
        else:
            # sort
            answers[key] = list(answers[key])       # convert to list
            answers[key].sort(key=int)              # sort
    return answers

queries = load_queries()
answers = boolean_retrieval_model(queries, inverted_index)


def save_results(answers):
    with open("Assignment1_21CS30059_results.txt", "w") as f:
        for key in answers:
            f.write(key + " : ")
            for value in answers[key]:
                f.write(value + " ")
            f.write("\n")

save_results(answers)






