from nltk.tokenize import RegexpTokenizer, TweetTokenizer
from stop_words import get_stop_words
import json
import string
from nltk.stem import WordNetLemmatizer
import sys
import nltk
from pyspark import SparkConf, SparkContext

min_review_length = 200
max_star = 2

# Initiate the spark context
conf = SparkConf().setMaster("local[*]").setAppName("My App")
sc = SparkContext(conf = conf)

# Create the key-value pair for business category
b_dict = sc.textFile("../../yelp_dataset/yelp_academic_dataset_business.json")
business = b_dict.map(json.loads).map(lambda x: (x["business_id"], x["categories"]))

rdd = sc.textFile("../../yelp_dataset/yelp_academic_dataset_review.json")
reviews = rdd.map(lambda x: json.loads(x))
# Only choose the long and negative review
reviews = reviews.filter(lambda x: x["stars"] <= max_star and len(x["text"].split()) > min_review_length)

# Only choose the reviews that makes to Chinese Restaurant
reviews = reviews.map(lambda x: (x["business_id"], x["text"])).join(business)
reviews = reviews.filter(lambda x: "Restaurants" in x[1][1] and "Chinese" in x[1][1])
reviews = reviews.map(lambda x: x[1][0])

# Natural Language Preprocessing transform texts to words
tokenizer = TweetTokenizer()
en_stop = get_stop_words('en')
wordnet_lemmatizer = WordNetLemmatizer()

tokens = reviews.flatMap(lambda x: tokenizer.tokenize(x.lower()))
no_punc_tokens = tokens.filter(lambda x: not x in string.punctuation+string.digits and not "." in x)
stop_tokens = no_punc_tokens.filter(lambda x: not x in en_stop)
stemmed_tokens = stop_tokens.map(lambda x: wordnet_lemmatizer.lemmatize(x))

# Counting the word frequency with map reduce and get the top 1000 
result = stemmed_tokens.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
high_freq = result.takeOrdered(1000, key = lambda x : -x[1])

# Output
outfile = open("../../high_freq_words_spark.txt", "w")
for h in high_freq:
	outfile.write(h[0])
	outfile.write("\n")
outfile.close()

sc.stop()


