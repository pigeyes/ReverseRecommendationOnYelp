from nltk.tokenize import TweetTokenizer
import pickle
import string
from stop_words import get_stop_words
from nltk.stem import WordNetLemmatizer
import gensim
import lda
import numpy as np
from gensim import corpora, models
import nltk
from nltk.corpus import wordnet as wn

infile = open("test_review.txt")
reviews = ' '.join([line for line in infile])
print "Done loading review, totally " + str(len(reviews.split())) + " words..."

# Load id term dictionary
infile = open("id_term_dictionary.pkl","r")
dictionary = pickle.load(infile)
infile.close()
print "Done loading dictionary..."

# Load trained lda model
infile = open("lda_model.pkl","r")
model = pickle.load(infile)
infile.close()
print "Done loading model..."

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
stemmed_tokens = [wordnet_lemmatizer.lemmatize(i, pos="v") for i in stopped_tokens ] 
stemmed_tokens = [wordnet_lemmatizer.lemmatize(i) for i in stemmed_tokens ] 

# Generate bi-gram
bi_grams = [i for i in nltk.bigrams(stemmed_tokens)]
bi_grams_sentence = [' '.join(s) for s in bi_grams]

# add tokens to list
dict_set = set(dictionary.values())
text = [s for s in bi_grams_sentence + stemmed_tokens if s in dict_set]

print "Done input preprocessing..."
# convert tokenized documents into a document-term matrix
corpus = dictionary.doc2bow(text)
dt_matrix = np.zeros((1, len(dictionary.values())), dtype=int)
for i in corpus:
    dt_matrix[0, i[0]] = i[1]
print "Done generate dt matrix..."

# Predict topics
reviews_topic = model.transform(dt_matrix, max_iter=1000)
vocab = tuple(t[1] for t in sorted(dictionary.items()))
n = 300
topic_words = np.array(vocab)[np.argsort(model.topic_word_[reviews_topic[0].argmax()])][:-(n+1):-1]
topic_words_dict = dict.fromkeys(topic_words, 0)
chosen_topic_words = []

for b in bi_grams_sentence:
    if str(b) in topic_words_dict:
        chosen_topic_words.append(str(b))
        break

for t in topic_words:
    syn = set()
    for synset in wn.synsets(t):
        for lemma in synset.lemmas():
            syn.add(' '.join(lemma.name().split("_")))
    for w in stemmed_tokens:
        if w in syn:
            # print t, ":", w, ":"
            # print syn
            topic_words_dict[t] += 1
            break

for d in sorted(zip(topic_words_dict.values(), topic_words_dict.keys()))[:-10:-1]:
    chosen_topic_words.append(d[1])

print('Predicted topic {}\n- {}'.format(reviews_topic[0].argmax(), ', '.join(chosen_topic_words).encode('utf-8')))






