# -*- coding:utf-8 -*-
import time
import os
#import re
#import requests
#import cv2
#import dlib
#import sys
#import threading
#import platform

name=input("输入文章标题：")
tag=input("输入分类：")
t=time.strftime('%Y-%m-%d',time.localtime(time.time()))
T=time.strftime('%Y-%m-%d %H:%m:%S',time.localtime(time.time()))
file_name=t+'-'+name+'.md'
#if 'Linux' in platform.platform():
#    os.system("touch ./_posts/"+file_name)
file=open("./_posts/"+file_name,'w')
file.write('---\nbg: "'+t+'.jpg"\nlayout: post\ntitle:  "'+name+'"\ncrawlertitle: "'+name+'"\nsummary: "'+name+'"\ndate:   '+T+' +0700\ncategories: posts\ntags: [\''+tag+'\']\nauthor: Chaf\n---')
file.close()

'''img=None

def img_show(img):
  cv2.imshow("pic",img)
  cv2.waitKey(0)

def show(img):
  th = threading.Thread(target=lambda:img_show(img))
  th.setDaemon(True)
  th.start()

def dowmloadPic(html, keyword):
  try:
    global img
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    print('找到关键词:' + keyword + '的图片，现在开始下载图片...')
    for each in pic_url:
        print('正在下载图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print('[错误]当前图片无法下载')
            continue

        dir = './assets/images/'+t+'.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        time.sleep(2)
        img = cv2.imread(dir)
        
        
        key=input("是否作为封面图片？y/n")
        return key
  except:
    print("图片下载失败")
    return 'n'


word = input("Input key word: ")
key='n'
pn=0
while key=='n':
  url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+word+'&pn='+str(pn)+'&gsm=3c&ct=&ic=0&lm=-1&width=0&height=0'
  result = requests.get(url)
  key=dowmloadPic(result.text, word)
  show(img)
  pn+=1'''

#os.system("typora "+file.name)
