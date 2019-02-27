# -*- coding:utf-8 -*-
import time
import os
name=input("输入文章标题：")
t=time.strftime('%Y-%m-%d',time.localtime(time.time()))
T=time.strftime('%Y-%m-%d %H:%m:%S',time.localtime(time.time()))
os.system("touch "+t+'-'+name+'.md')
file=open(t+'-'+name+'.md','r+')
file.write('---\nbg: "'+t+'.jpg"\nlayout: post\ntitle:  "'+name+'"\ncrawlertitle: "'+name+'"\nsummary: "'+name+'"\ndate:   '+T+' +0700\ncategories: posts\ntags: [\''+name+'\']\nauthor: Chaf\n---')
file.close()

os.system("typora "+file.name)
