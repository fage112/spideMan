#!/bin/python
#python版本：python3
#用于爬取https://www.shanbay.com网的6级英语单词词汇
#coding: utf-8
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import pickle,pymysql
import re
class spide():
    def __init__(self,InitPage,method):
        self.M_queue=[]
        self.S_queue=[]
        self.seen=[]
        self.InitPage=InitPage
        self.method=method
    def request(self,url,data=''):
        #网络请求
        if self.method=='post':
            data = parse.urlencode(data)
            data = data.encode('ascii')
            if not data:
                req = request.Request(url, data)
            with request.urlopen(req) as response:
                page=response.read()
                return page.decode('utf-8')
        if self.method=='get':
            if not data:
                url_values = parse.urlencode(data)
                full_url = url + '?' + url_values
            else:
                full_url=url
            with request.urlopen(full_url) as response:
                page=response.read()
                return page.decode('utf-8')
    def queue(self,data):
        #爬取需要的url
        M_queue_re = re.compile('href="(/wordlist/176893/\d*/)"')
        Word_count=re.compile('<span>单词数：</span>(\d+)')
        for x in M_queue_re.findall(data):
            self.M_queue.append(x)
        for i in Word_count.findall(data):
            self.S_queue.append(i)
def storage(data,tbname):
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='*******',
                           db='english',
                           charset='utf8')
    cursor = conn.cursor()
    sql1='CREATE TABLE IF NOT EXISTS '+tbname+''' (
  word varchar(255) NOT NULL,
  mean varchar(512) DEFAULT NULL,
  memo varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
    print(sql1)
    cursor.execute(sql1)
    for k, v in data.items():
        sql = 'INSERT INTO %s (word,mean) VALUES ( "%s", "%s")'
        data1 = (tbname, k, v)
        try:
            cursor.execute(sql % data1)
            conn.commit()
        except pymysql.err.ProgrammingError as e:
            print(e)
            print(str(k), str(v))
            continue
    conn.close()
def start(url,method):
    words=[]
    means=[]
    domain='https://www.shanbay.com'
    a=spide(url,method)
    a.queue(a.request(a.InitPage))
    Queue=dict(zip(a.M_queue,a.S_queue))
    for k in Queue.keys():
        N = int(int(Queue[k])/20)
        if int(Queue[k])%20!=0:
            N = N + 1
        for i in range(1,N):
            data='?'+'page='+str(i)
            url=domain+k+data
            print('正在爬取'+url)
            page=a.request(url,data)
            soup=BeautifulSoup(page,'lxml')
            Sum = 1
            for i in soup.table.stripped_strings:
                if Sum % 2 == 1:
                    words.append(i)
                else:
                    means.append(i)
                Sum += 1
    word_dic = dict(zip(words,means))
    storage(word_dic,'cet6')
if __name__=="__main__":
    start('https://www.shanbay.com/wordbook/176893/','get')