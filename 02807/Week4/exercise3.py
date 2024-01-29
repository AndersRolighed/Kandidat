import sys
import os
import mmh3


def listhash(l, seed):
    hash_list = []
    val = 0
    for e in l:
        val = val ^ mmh3.hash(e, seed)
        hash_list.append(val)
    return hash_list

replace_tokens = [".", ",", "?",":",";","!"]
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
    for i in range(k):
        hash = listhash(shingles,seed*i)
        min_hash = min(hash)
        min_hashes.append(min_hash)

    return min_hashes



string = "heya im an all star. Get your groove on, come on! This is fun. Yes. Yes. Yes. Yes. No!"

q = 3
k = 100
seed = 10 ## Gets multiplied by 1:k
shingles = create_shingles(string,q)
min_hashes = minhash(shingles, seed, k)
print(min_hashes)