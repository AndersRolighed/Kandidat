import numpy as np

string = "heya im an all star. Get your groove on, come on! This is fun. Yes. Yes. Yes. Yes. No!"

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
    shingles_set = set(tuple(row) for row in shingles_list)
    return shingles_set

string2 = create_shingles(string,3)
print(string2)
