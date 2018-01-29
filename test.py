#!/bin/env python
#在数据库中随机查询5个单词，显示，记住后回答正确后退出程序
import pymysql
import os
def cls():
    os.system('cls')
class words_test():
    def __init__(self):
        self.mysql_host='localhost'
        self.mysql_user='root'
        self.mysql_password='*******'
        self.db='english'
    def random_select(self):
        conn=pymysql.connect(host=self.mysql_host,user=self.mysql_user,
                             password=self.mysql_password,db=self.db,charset='utf8')
        with conn.cursor() as cursor:
            sql='SELECT word,mean FROM computer ORDER BY RAND() LIMIT 5;'
            cursor.execute(sql)
            result=cursor.fetchall()
            conn.close()
        words_list=[]
        for i in result:
            words_list.append(i)
        return words_list
    def test(self,words_list):
        for i in range(len(words_list)):
            print(words_list[i][0])
            print(words_list[i][1])
            input('记住单词后请输入按回车键:')
            cls()
            while True:
                word = input('请输入单词:')
                if word.lower()==words_list[i][0].lower():
                    break
                elif word.lower()=='replay':
                    print(words_list[i][0])
                    print(words_list[i][1])
                    input('记住单词后请输入按回车键:')
                    cls()
                else:
                    print('单词拼写不对，请重新输入:')
        print('恭喜你，今天又记住了5个单词，一定要坚持每天练习哦！')
if __name__=='__main__':
    a=words_test()
    b=a.random_select()
    a.test(b)