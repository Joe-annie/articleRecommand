import sys
sys.path[0]='/usr/local/lib/python3.7/site-packages'
import pymongo
import json
import jieba
hostname = "127.0.0.1"
port_num = int("27017")
db_name = "articleExtract"
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
import pandas as pd
import numpy as np

try:
    client = pymongo.MongoClient(hostname, port_num)
    db = client[db_name]
except:
    print("connection wrong")

jieba.load_userdict('mydic.txt')
stop = [line.strip()  for line in open('stopwords.txt').readlines() ]

def cutWords_search(msg, stopWords):
    seg_list = jieba.cut_for_search(msg)    
    txtWords = ""    
    for i in seg_list:
        #过滤stop words       
        if (i not in stopWords):            
            txtWords = txtWords + i + ' '          
    return txtWords
def cutWords(msg, stopWords):
    seg_list = jieba.cut(msg,cut_all=False)    
    txtWords = ""    
    for i in seg_list:
        #过滤stop words       
        if (i not in stopWords):            
            txtWords = txtWords + i + ' '          
    return txtWords
def tfi(size):
    tfidf = TfidfVectorizer(sublinear_tf=True,norm='l2', min_df=6,encoding='latin-1', 
                    )
    features = tfidf.fit_transform(txtlist_cut).toarray()
    names = np.array(tfidf.get_feature_names())
    # print(tfidf.vocabulary_)
    if size > features.shape[1]:return False
    for row in range(0,features.shape[0]):
        onerow = features[row,]
        idx = np.argpartition(onerow, -size)[-size:]
        oneFeature = names[idx]
        featurelist.append(oneFeature)


collection = db.Symposium # update collection
txtlist_cut = []
featurelist = []
for doc in collection.find():
    txt_str = doc['title']
    txt_str = ''.join(list(filter(lambda x: x.isalpha(), txt_str)))
    # update jieba cut for search
    article_search = cutWords_search(txt_str, stop)
    doc['title_forsearch'] = article_search
    condition = {'_id':doc['_id']}
    result = collection.update_one(condition,{'$set':doc})
    

