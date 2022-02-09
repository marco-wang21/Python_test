# @File  : dqd_comment_clean.py
# @Author: Marco Wang
# @Date  :  2022/02/09

# -- coding: utf-8 --
import re
f = open('dqd3.txt',encoding='utf-8')
text = f.read()

import jieba
text_list = jieba.lcut(text) #分词
text_str = ' '.join(text_list)
# jieba.add_word("唐佳丽")
# jieba.add_word("退钱")
# jieba.add_word("rnm退钱")
# jieba.add_word("脸都不要了")
# jieba.add_word("青训")
# jieba.add_word("日你妈")
# jieba.add_word("规化")
# jieba.add_word("归化")
# jieba.add_word("程序员")
# jieba.add_word("范志毅封神")
# jieba.add_word("李铁对不起")
# jieba.add_word("范志毅牛逼")
# jieba.add_word("李霄鹏下课")
# jieba.add_word("范大将军")
# jieba.add_word("软脚虾")
# jieba.add_word("吴佳丽")
# jieba.add_word("牛逼")
# jieba.add_word("人球分过")
# jieba.add_word("头球")
# jieba.add_word("铿锵玫瑰")
# jieba.add_word("亚洲之巅")
# jieba.add_word("让二追三")

stoplist = [i.strip() for i in open('stoplist.txt', encoding = 'utf-8').readlines()]   #stoplist
def m_cut(intxt):  #segmentation
    word = [w for w in jieba.cut(intxt) if w not in stoplist and len(w) > 1 and not re.match('^[a-z|A-Z|0-9|哈|啊|足球|.]*$',w)]
    strword = " ".join(word)
    return strword

cuttext = m_cut(text)

import wordcloud
import imageio  #根据本地图片修改词云图形
img2 = imageio.imread('tree.png')
wc = wordcloud.WordCloud(
    width=200,
    height=200,
    background_color = 'white',
    mask=img2 ,
    stopwords={'姑娘','球员','女足','越南'},
    font_path = 'msyh.ttc',
    collocations=False
)
wc.generate(cuttext)
wc.to_file('女足.png')