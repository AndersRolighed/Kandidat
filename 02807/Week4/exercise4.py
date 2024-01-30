import sys
import os
import mmh3
import scipy
import sklearn
import numpy as np
import random
from itertools import combinations


def listhash(l, seed):
    hash_list = []
    for e in l:
        val = 0
        for m in e.split(" "):
            val = val ^ mmh3.hash(m, seed)
        hash_list.append(val)
    return hash_list

replace_tokens = [".", ",", "?",":",";","!","\n"]
def create_shingles(string,q):
    string = string.replace("  ", " ")
    for token in replace_tokens:
        string = string.replace(token,"")
    
    string = string.split(" ")
    shingles_list = []
    for k in range(len(string)-q+1):
        shingle = string[k:q+k]
        shingles_list.append(shingle)
    shingles_set_tuples = set(tuple(row) for row in shingles_list)

    shingles_list = []
    for string_tuple in shingles_set_tuples:
        shingle = " ".join([word for word in string_tuple])
        shingles_list.append(shingle)
    
    return shingles_list

def minhash(shingles,seed,k):
    min_hashes = []
    for l in range(k):
        hash = listhash(shingles,l)
        min_hash = min(hash)
        min_hashes.append(min_hash)

    return min_hashes

def signatures(documentID):
    docs_signatures = {}
    document_txt = docs[documentID]
    shingles = create_shingles(document_txt,q)
    min_hashes = minhash(shingles,seed,k)
    docs_signatures[documentID] = min_hashes
    return docs_signatures


def jaccard_similarity(A, B):
    nominator = A.intersection(B)

    denominator = A.union(B)
    
    if len(nominator) == 0 or len(denominator) == 0:
        similarity = 0
    else:
        similarity = len(nominator)/k
    
    return similarity

################### Similarity ######################
q = 3 # length of shingle
k = 100 # number of minhashes
seed = 100 ## Gets multiplied by 1:k
docs = {} #dictionary mapping document id to document contents
# read data sets
srcfolder = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(srcfolder, "DataWeek5/ats_corpus_small")   # change to ats_corpus for large data set

for file in os.listdir(datafolder):
    filepath = os.path.join(datafolder, file)
    f = open(filepath, 'r')
    docs[file] = f.read()
    print("read document " + file)
    f.close()


def jaccard(documents):
    doc1 = documents[0]
    doc2 = documents[1]
    signature1 = signatures(doc1)[documents[0]]
    signature2 = signatures(doc2)[documents[1]]
    similarity = jaccard_similarity(set(signature1), set(signature2))
    print(similarity)

    return similarity

def similar(documents):
    similarity_doc = {}
    similar_doc = {}
    doc_combinations = list(combinations(documents,2))
    for i in range(len(doc_combinations)):
        docs1 = doc_combinations[i][0]
        docs2 = doc_combinations[i][1]
        similar_score = jaccard([docs1,docs2])
        similarity_doc[doc_combinations[i]] = similar_score
        if similar_score >= 0.6:
            similar_doc[doc_combinations[i]] = similar_score
    

    return similarity_doc, similar_doc

similarity_doc, similar_doc = similar(list(docs.keys()))
#print(similarity_doc)

#print(similar_doc)
#similar(list(docs.keys))
#shingles = create_shingles(string,q)
#min_hashes = minhash(shingles, seed, k)
#print(min_hashes)

#print(create_shingles(docs["calltounconv00baxt.txt"],3))