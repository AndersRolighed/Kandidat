import string
from functools import reduce

def count_words(word_list, document_id):
    return reduce(lambda word_dict, word: {**word_dict, word: word_dict.get(word, {'count': 0, 'docs': set()})}, 
                  word_list, 
                  {'document_id': document_id}
                )

def update_word_dict(word_dict, document_id):
    return {**word_dict, 'count': word_dict['count'] + 1, 'docs': word_dict['docs'].union({document_id})}

def get_word_frequencies(documents):
    all_words = {}

    for doc_id, document_path in enumerate(documents):
        with open(document_path, 'r') as file:
            text = file.read().lower()
            translator = str.maketrans('', '', string.punctuation)
            text = text.translate(translator)
            words = text.split()
            word_dict = count_words(words, doc_id)
            
            for word, info in word_dict.items():
                if word != 'document_id':
                    all_words[word] = update_word_dict(all_words.get(word, {'count': 0, 'docs': set()}), doc_id)
    
    return all_words

documents = ['TestExercise2.txt', 'TestExercise3.txt', 'TextExercise4.txt']  # Replace with actual paths of your documents
frequencies = get_word_frequencies(documents)

for word, info in frequencies.items():
    count = info['count']
    docs = info['docs']
    print(f'{word}: Count - {count}, Documents - {docs}')
