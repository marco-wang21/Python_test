# @File  : mda.py
# @Author: Marco Wang
# @Date  :  2022/02/03

# -- coding: utf-8 --

import pandas as pd
c = pd.read_excel('./管理层讨论与分析.xlsx')  #MD&A Data comes from CNRDS
c.columns=c.iloc[0].values
c = c.drop(0)
import jieba
import re

stoplist = [i.strip() for i in open('stoplist.txt', encoding = 'utf-8').readlines()]   #stoplist

def m_cut(intxt):  #segmentation
    word = [w for w in jieba.cut(intxt) if w not in stoplist and len(w) > 1 and not re.match('^[a-z|0-9|%|.]*$',w)]
    strword = " ".join(word)
    return strword


d = pd.read_csv('./代码.csv')  #industry classification
d1 = d.drop_duplicates(subset=['Stkcd'], keep='first')
d1['Stkcd'] = d1['Stkcd'].astype('str')
d1['Stkcd'] = d1['Stkcd'].str.zfill(6)
d1 = d1.rename(columns={'Stkcd':'股票代码'})


data = pd.merge(c, d1, how = 'left')

data = data[data["会计年度"] == '2020']  #only keep Year2019
data1 = data.drop_duplicates(subset=['股票代码','会计年度'], keep='last')



data1 = data1.reset_index()
data1=data1.drop(labels=['index'],axis=1)
alist = data1['经营讨论与分析内容'].to_list()

import time

blist = []
time_start = time.time()
for i in range(len(alist)):
    print(i)
    x = m_cut(alist[i])
    blist.append(x)
print(time.time() - time_start)

df2 = pd.DataFrame(blist)
df2 = df2.rename(columns={0:'cut'})
data1 = pd.concat([data1, df2], axis=1)
clist = []
clist=data1['cut'].values.tolist()
text_str = ' '.join(clist)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_tf_idf_vectors(corpus):  #text vectorization
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_results = tfidf_vectorizer.fit_transform(corpus).todense()
    return tfidf_results

tf_idf_vectors = get_tf_idf_vectors(clist)

clist= []
for i in range(0,4262):  #the total number of listed company in 2019
    a = cosine_similarity(tf_idf_vectors[i],tf_idf_vectors[2198])[0][0]  #300263的位置
    clist.append(a)

data1.insert(loc=0, column='Cosine', value=clist)
data2 = pd.DataFrame(data1, columns=['股票代码','公司简称','Cosine','Indcd','文字数量'])
data2 = data2.sort_values(by=['Cosine'],ascending=False)
data2.to_csv('MD&A.csv',index=False,encoding='utf_8') #save
# wc = wordcloud.WordCloud(   #wordcloud
#     width=500,
#     height=500,
#     background_color = 'white',
#     mask=img2 ,
#     stopwords={'公司','子公司','有限公司','产品','客户','风险','行业','经营','收入'},
#     font_path = 'msyh.ttc',
#
# )
# wc.generate(blist[4066])
# wc.to_file('世华科技.png')
#
# data1.loc[data1['股票代码'] == '688093']  #find