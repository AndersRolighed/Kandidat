import string
from functools import reduce

def count_words(word_list):
    return reduce(lambda word_dict, word: {**word_dict, word: word_dict.get(word, 0) + 1}, word_list, {})

def get_word_frequencies(document_path):
    with open(document_path, 'r') as file:
        text = file.read().lower()
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        words = text.split()
        return count_words(words)

document_path = 'TestExercise2.txt'
frequencies = get_word_frequencies(document_path)

for word, frequency in frequencies.items():
    print(f'{word}: {frequency}')
