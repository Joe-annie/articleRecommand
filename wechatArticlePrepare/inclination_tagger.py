import sys
sys.path[0]='/usr/local/lib/python3.7/site-packages'
import pymongo
import json
import jieba
hostname = "127.0.0.1"
port_num = int("27017")
db_name = "articleExtract"

try:
    client = pymongo.MongoClient(hostname, port_num)
    db = client[db_name]
except:
    print("connection wrong")

#print(collection.find().count())

#添加search属性
# def cutWords(msg, stopWords):
#     seg_list = jieba.cut_for_search(msg)    
#     #use list to store words
#     #txtWords = [] 
#     #use string to store words
#     txtWords = ""    
#     for i in seg_list:
#         #过滤stop words       
#         if (i not in stopWords):            
#             #txtWords.append(i) 
#             txtWords = txtWords + i + ' '          
#     return txtWords

# jieba.load_userdict('mydic.txt')
# stop = [line.strip()  for line in open('stopwords.txt').readlines() ]

# for doc in collection.find():
#     # upate jieba cut
#     txt_str = doc['article']
#     txt_str = ''.join(list(filter(lambda x: x.isalpha(), txt_str)))
#     onecut = cutWords(txt_str, stop)
#     doc['search'] = onecut
#     condition = {'_id':doc['_id']}
#     result = collection.update_one(condition,{'$set':doc})

# result = collection.aggregate([
#     {' $match': { '$or': [ { 'title': { '$regex':"乳腺癌"} }, {'title':{'$regex':"补钙"}} ]  }
#     }
# ])
# result = list(result)


setdic_female = {'gender':'F'}
setdic_male = {'gender': 'M'}

condition_female = { '$or': [ { 'title': { '$regex':"妈妈"} }, { 'title':{'$regex':"女性"} }, { 'title':{'$regex':"乳腺癌"} }, { 'title':{'$regex':"怀孕"} }   ]  }
condition_male = { '$or': [ { 'title': { '$regex':"男性"} }, { 'title':{'$regex':"男人"} }, { 'title':{'$regex':"前列腺"} }    ]  }

setdic_spring = {'season':'Spring'}
setdic_summer = {'season': 'Summer'}
setdic_autumn= {'season':'Autumn'}
setdic_winter = {'season': 'Winter'}
condition_spring = { '$or': [ { 'title': { '$regex':"春"} } ]  }#春雨医生#match 
condition_summer = { '$or': [ { 'title': { '$regex':"夏"} } ]  }
condition_autumn = { '$or': [ { 'title': { '$regex':"秋"} } ]  }
condition_winter = { '$or': [ { 'title': { '$regex':"冬"} } ]  }

setdic_child = {'age':'Child'}
setdic_elder = {'age': 'Elder'}
condition_child = { '$or': [ { 'title': { '$regex':" 宝宝"} }, { 'title':{'$regex':"孩子"} }, { 'title':{'$regex':"婴儿"} }    ]  }
condition_elder = { '$or': [ { 'title': { '$regex':"老人"} }, { 'title':{'$regex':"老年"} }   ]  }


trends = [
    {'setdic': setdic_female, 'condition': condition_female },
    {'setdic': setdic_male, 'condition': condition_male },

    {'setdic': setdic_spring, 'condition': condition_spring },
    {'setdic': setdic_summer, 'condition': condition_summer },
    {'setdic': setdic_autumn, 'condition': condition_autumn },
    {'setdic': setdic_winter, 'condition': condition_winter },

    {'setdic': setdic_child, 'condition': condition_child },
    {'setdic': setdic_elder, 'condition': condition_elder },
]

collection = db.CYYSweb_article #collection name,where title from
coll = db.CYYSweb_keywords # update collection
#init collection
# coll.update_many({'_id' : {'$exists': True}}, {'$set':{'gender':'N', 'season':'N', 'age':'N'}})
#忽略春雨关键词
# coll.update_many({ 'title': { '$regex':"春雨"} }, {'$set':{ 'season':'N'}})

for dic in trends:
    result = collection.find(dic['condition'])    
    for doc in result:
        # titles.append(doc['title'])
        # wechat version：
        condition = {'id': str(doc['_id']) }
        # condition = {'id':doc['id']}
        output = coll.update_many(condition,{'$set':dic['setdic']})
        print(output.matched_count,output.modified_count)
    
# result = coll.find(setdic_spring).count()
# print(result)