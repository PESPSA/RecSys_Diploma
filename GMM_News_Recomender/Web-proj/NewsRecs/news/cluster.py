import json
import os
import random
import re
import string

import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from nltk.stem import WordNetLemmatizer

from scipy import spatial
from scipy.spatial.distance import cosine
import pickle

regex = re.compile(u"[A-Za-z]+")

def words_only(text, regex=regex):
    return " ".join(regex.findall(str(text)))


# Удаляем стоп-слова
mystopwords = stopwords.words('english') + ['-', '-']

def remove_stopwords(text, mystopwords=mystopwords):
    try:
        return u" ".join([token for token in text.split() if not token in mystopwords])
    except:
        return u""

# нормализуем текст
wordnet_lemmatizer = WordNetLemmatizer()
def lemmatize(text, lemmatizer=wordnet_lemmatizer):
    word_list = nltk.word_tokenize(text)
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
    return lemmatized_output

def randomword(length):
   letters = string.ascii_uppercase
   return ''.join(random.choice(letters) for i in range(length))

def id_gen():
    start_str = "MY"
    return start_str+randomword(5)

flag1 = 0

def get_nearest_clusters(cluster_num):
    global flag1
    if flag1 == 0:
        with open("C:/diploma/Web-proj/NewsRecs/data/cluster_centers.json") as f:
            global cluster_centers
            cluster_centers = json.load(f)
        flag1 = 1
    dist = []
    for i in range(len(cluster_centers)):
        pairwise_dist = cosine(cluster_centers[cluster_num], cluster_centers[i])
        dist.append([pairwise_dist, i])
    dist = sorted(dist, key=lambda d: d[0])[:3]
    res = []
    for i in range(len(dist)):
        if dist[i][0] <= 0:
            res.append(dist[i][1])
    return res


def cluster_news(body, abstract, subcategory):
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    dir = dir.replace('news', 'data')
    os.chdir(dir)

    news = body + abstract + subcategory
    news = lemmatize(remove_stopwords(words_only(news.lower())))
    tf_idf = pickle.load(open("tfidf.pkl", 'rb'))
    SVD = pickle.load(open("SVD.pkl", 'rb'))
    GMM = pickle.load(open("GMM.pkl", 'rb'))
    X_news = tf_idf.transform([news])
    truncated_X_news = SVD.transform(X_news)
    label = GMM.predict(truncated_X_news)
    return label[0]
