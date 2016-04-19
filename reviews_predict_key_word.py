from nltk.tokenize import TweetTokenizer
import string
from stop_words import get_stop_words
from nltk.stem import WordNetLemmatizer
import gensim
import nltk
from nltk.corpus import wordnet as wn

#General keyword
#key_words = [line[:-1] for line in open("keyword_map_general.txt")]
#key_bigrams = [line[:-1] for line in open("high_frequency_bigrams.txt")][1:]
#Build keyword map
key_map = {}
for k in open("keyword_map_general.txt"):
    a = k.strip().split(", ")
    key_map[a[0]] = a[1]

#Special keyword
#special_words = [line[:-1] for line in open("keyword_map_special.txt")]
#Build keyword map
special_map = {}
for k in open("keyword_map_special.txt"):
    a = k.strip().split(", ")
    special_map[a[0]] = a[1]

infile = open("test_review.txt")
reviews = ' '.join([line for line in infile])

print "Finish reading text"

# Preprocessing the input reviews
# clean and tokenize document string
raw = reviews.lower()
tokenizer = TweetTokenizer()
tokens = tokenizer.tokenize(raw)

# remove punctuations
no_punc_tokens = [i for i in tokens if (not i in string.punctuation+string.digits) and (not "." in i)]

# remove stop words from tokens
en_stop = get_stop_words('en')
stopped_tokens = [i for i in no_punc_tokens if not i in en_stop]

# stem tokens
#stemmed_tokens = [wordnet_lemmatizer.lemmatize(i, pos="v") if "V" in nltk.pos_tag(i) else wordnet_lemmatizer.lemmatize(i) 
                  #for i in stopped_tokens ] 
wordnet_lemmatizer = WordNetLemmatizer()
#stemmed_tokens = [wordnet_lemmatizer.lemmatize(i, pos="v") for i in stopped_tokens ] 
stemmed_tokens = [wordnet_lemmatizer.lemmatize(i) for i in stopped_tokens ] 

# Generate bi-gram
# bi_grams = [i for i in nltk.bigrams(stemmed_tokens)]
# bi_grams_sentence = [' '.join(s) for s in bi_grams]

print "Finish preprocessing text"

chosen_key_words = []

# Search in general key word
key_words_dict = dict.fromkeys(key_map.values(), 0)
# Select keyword using wordnet
"""
for t in key_map.keys():
    syn = set()
    for synset in wn.synsets(t):
        for lemma in synset.lemmas():
            syn.add(' '.join(lemma.name().split("_")))
    for w in stemmed_tokens:
        if w in syn:
            key_words_dict[key_map[t]] += 1
"""

# Select keyword use only key word to select
s = set(stemmed_tokens)
for t in key_map.keys():
    if t in s:
        key_words_dict[key_map[t]] += 1

# for t in bi_grams_sentence:
#     if str(t) in key_bigrams:
#         chosen_key_words.append(str(t))
#         break

for d in sorted(zip(key_words_dict.values(), key_words_dict.keys()))[:-4:-1]:
    if d[0] > 0:
        chosen_key_words.append(d[1])

# Search in special keyword
special_words_dict = dict.fromkeys(special_map.values(), 0)
#  Select keyword using wordnet
"""
for t in special_map.keys():
    syn = set()
    for synset in wn.synsets(t):
        for lemma in synset.lemmas():
            syn.add(' '.join(lemma.name().split("_")))
    for w in stemmed_tokens:
        if w in syn:
            special_words_dict[special_map[t]] += 1
"""

# Select keyword use only key word to select
s = set(stemmed_tokens)
for t in special_map.keys():
    if t in s:
        special_words_dict[special_map[t]] += 1

# for t in bi_grams_sentence:
#     if str(t) in key_bigrams:
#         chosen_key_words.append(str(t))
#         break

for d in sorted(zip(special_words_dict.values(), special_words_dict.keys()))[:-3:-1]:
    if d[0] > 0:
        chosen_key_words.append(d[1])

print chosen_key_words
