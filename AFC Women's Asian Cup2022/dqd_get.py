# @File  : dqd2.py
# @Author: Marco Wang
# @Date  :  2022/02/04

# -- coding: utf-8 --
import json
import requests


def get_content(url_new):
    url = url_new
    dic = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    json_data1 = requests.get(url, headers=dic)
    b = json_data1.json()
    return b

def get_comment(b):
    url_new1 = b['data']['next']
    blist = []
    for i in range(0, len(b['data']['comment_list'])):
        blist.append(b['data']['comment_list'][i]['content'])
    strr1 = '\n'.join(blist)
    return url_new1, strr1


def firstline():
    url = 'https://www.dongqiudi.com/api/v2/article/2572164.html/comment?size=20&platform=web'   #https://www.dongqiudi.com/articles/2572164.html
    dic = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.34"
    }
    json_data = requests.get(url, headers=dic)
    a = json_data.json()
    url_new = a['data']['next']
    alist = []
    for i in range(0, len(a['data']['comment_list'])):
        alist.append(a['data']['comment_list'][i]['content'])
    strr = '\n'.join(alist)
    return strr, url_new

import time

def main():
    clist = []
    strr , url_new = firstline()
    clist.append(strr)
    for i in range(0,100000):
        try:
            b = get_content(url_new)
            url_new1 ,strr1 = get_comment(b)
            clist.append(strr1)
            url_new = url_new1
            print("第{}页完毕".format(i))
            print(url_new)


        except:

            break
    for index in clist:
        with open('dqd3.txt', mode='a', encoding='utf-8') as f:
            f.write(index)
            f.write('\n')



if  __name__ == '__main__':
    main()

