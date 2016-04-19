from nltk.tokenize import RegexpTokenizer, TweetTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import json
import string
import numpy as np
import lda
from nltk.stem import WordNetLemmatizer
import sys
import nltk
import pickle

# Set up the parameter
max_reviews = 5000
num_topic = 8
num_iteration = 1000
min_review_length = 200
max_star = 2

# Top 500 words in Chinese, Restaurant, with <= 1, > 100 words
my_stop_words = [line[:-1] for line in open("my_stop_words.txt")][1:]

# Top 500 words in Chinese, Restaurant, with <= 1, > 100 words
my_bigram_stop_words = [line[:-1] for line in open("my_stop_bigrams.txt")][1:]

tokenizer = TweetTokenizer() #RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
#p_stemmer = PorterStemmer()

wordnet_lemmatizer = WordNetLemmatizer()

# Load business json
file2 = open("yelp_academic_dataset_business.json")
b_dict = {}
business = [json.loads(line) for line in file2]
for b in business:
    b_dict[b["business_id"]] = {"categories":b["categories"], "city":b["city"]}

# Load documents into a list
file1 = open("yelp_academic_dataset_review.json")
doc_set = []
id_set = []
reviews_size = 0
reviews = json.loads(file1.readline())
idx = 0
while reviews:
    if reviews_size > max_reviews:
        break 
    print "Got " + str(reviews_size) + " valid reviews......\r",
    if (reviews["stars"] <= max_star and len(reviews["text"].split()) > min_review_length 
        and "Restaurants" in b_dict[reviews["business_id"]]["categories"]
        and "Chinese" in b_dict[reviews["business_id"]]["categories"]):
        doc_set.append(reviews["text"])
        id_set.append(idx)
        reviews_size += 1
    try :
        reviews = json.loads(file1.readline())
    except ValueError:
        reviews = None
    idx += 1
print ""

# list for tokenized documents in loop
texts = []

# loop through document list
count = 0
for i in doc_set:

    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove punctuations
    no_punc_tokens = [i for i in tokens if (not i in string.punctuation+string.digits) and (not "." in i)]

    # remove stop words from tokens
    stopped_tokens = [i for i in no_punc_tokens if not i in en_stop]

    # stem tokens
    #stemmed_tokens = [wordnet_lemmatizer.lemmatize(i, pos="v") if "V" in nltk.pos_tag(i) else wordnet_lemmatizer.lemmatize(i) 
                      #for i in stopped_tokens ] 
    stemmed_tokens = [wordnet_lemmatizer.lemmatize(i, pos="v") for i in stopped_tokens ] 
    stemmed_tokens = [wordnet_lemmatizer.lemmatize(i) for i in stemmed_tokens ] 

    # Remove my stop words from stem tokens
    my_stopped_tokens = [i for i in stemmed_tokens if not i in my_stop_words]
    
    # Generate bi-gram
    bi_grams = [i for i in nltk.bigrams(stemmed_tokens)]
    bi_grams_sentence = [' '.join(s) for s in bi_grams]
    my_stopped_bigram = [i for i in bi_grams_sentence if not i in my_bigram_stop_words]

    # add tokens to list
    texts.append(my_stopped_bigram*2 + my_stopped_tokens )
    
    count += 1
    print "Processed " + str(count) + " reviews......\r",
print ""

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
outfile = open("id_term_dictionary.pkl", "w")
pickle.dump(dictionary, outfile)
outfile.close()
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]
dt_matrix = np.zeros((reviews_size, len(dictionary.values())), dtype=int)
for i in xrange(len(corpus)):
    for p in corpus[i]:
        dt_matrix[i, p[0]] = p[1]

# generate LDA model
#ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=4, id2word = dictionary, passes=10)
#print(ldamodel.print_topics(num_topics=4, num_words=4))

model = lda.LDA(n_topics=num_topic, n_iter=num_iteration, random_state=1)
model.fit(dt_matrix)
outfile = open("lda_model.pkl", "w")
pickle.dump(model, outfile)
outfile.close()

# Visualize the result

vocab = tuple(t[1] for t in sorted(dictionary.items()))

print "============== Top words for every topics ================"
outfile = open("top_words_of_topics.txt", "w")
topic_word = model.topic_word_
# Make the high freq terms not too strong
# column_sum = np.sum(topic_word, axis=0) + 0.01
# topic_word = topic_word / column_sum
n = 20
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    print('*Topic {}\n- {}'.format(i, ', '.join(topic_words).encode('utf-8')))
    outfile.write('*Topic {}\n- {}'.format(i, ', '.join(topic_words).encode('utf-8')))
    outfile.write("\n")
outfile.close()

#print "============== Topics of documents ================"
outfile = open("topics_of_documents.txt", "w")
doc_topic = model.doc_topic_
for n in xrange(len(texts)):
    topic_most_pr = doc_topic[n].argmax()
    #print("doc: {} topic: {}".format(id_set[n], topic_most_pr))
    outfile.write("doc: {} topic: {}".format(id_set[n], topic_most_pr))
    outfile.write("\n")
outfile.close()

# Analysis of frequent word
print "============== Most frequent words ================"
# co_sum = [(sum(dt_matrix[:, i]), i) for i in xrange(len(dt_matrix[0,:]))]
# # for t in sorted(co_sum)[:-500:-1]:
# # 	print '{0:10s}: {1:4d}'.format(dictionary[t[1]], t[0])

# outfile = open("high_frequency_bigrams.txt", "w")
# count = 0
# for t in sorted(co_sum)[:-1000:-1]:
# 	outfile.write(dictionary[t[1]].encode('utf-8'))
# 	outfile.write("\n")
# 	# if count % 10 == 9:
# 	# 	print ""
# 	# count += 1
# outfile.close()










