---
layout: post
title: Wechat Robot
subtitle: USTC Python and Deep Learning Course 2019 Project
thumbnail-img: /assets/images/thumbnail-img/wechatRobot.jpg
cover-img: /assets/images/cover-img/wechatRobot.jpg
comments: true
gh-repo: Chaphlagical/WeChat-Robot
gh-badge: [star, fork, follow]
tags: [Python, AI]
readtime: true
---

Python and Deep Learning Course 2019 Spring Project

## 一、概览

以Python的微信接口库wxpy为基础，通过微信端人机交互，实现不同丰富的功能。**项目地址：[https://github.com/Chaphlagical/WeChat-Robot](https://github.com/Chaphlagical/WeChat-Robot)**

## 二、功能简介

### （一）朋友圈数据分析

#### 1、基本原理

##### （1）jieba

用于分词以生成好友个性签名词云

##### （2）pyecharts

用于可视化数据

#### 2、文件结构

##### （1）./analysis/user_analysis.py

用户好友数据分析类User_Friends

##### （2）./analysis/group_analysis.py

好友群组数据分析类User_Group

##### （3）./analysis/tools.py

基础预处理函数（例如排序、统计、字符串操作等）

##### （4）./scripts/function/analysis.py

対各个数据分析函数再进行一次上层封装

#### 3、基本使用方法

运行程序，扫码登陆微信，在任意一个聊天里，输入：

```
analysis friends
```

电脑端程序开始运行，

生成以下文件（夹）

- `./data/user/avatar`保存好友头像，
- markdown文件`./data/user/user_friends_data.md`保存好友的备注、昵称、地区、头像、性别等信息，
- html文件`./data/user/Graph/China.html`记录好友在中国的分布
- html文件`./data/user/Graph/Gender.html`可视化好友的性别比例
- html文件`./data/user/Graph/Signature.html`可视化好友个性签名词云
- html文件`./data/user/Graph/province.html`记录好友所在人数最多省份的具体分布

输入：

```
check friend [-好友名]
```

将显示好友的基本信息

输入：

```
analysis group [-群组名]
```

或者分析所有群组（时间较长，不推荐）：

```
analysis all group
```

生成以下文件（夹）：

- `./data/group/[group_name]/group_members_data.md `保存群组成员的信息
- `./data/group/[group_name]/avatar`保存群组成员头像
- `./data/group/[group_name]/Graph/Relationship.html`群组成员关系可视化

输入：

```
check group [-群组名]
```

将显示群组的基本信息

#### 效果

html文件已保存为图片

![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/3.jpg){: .mx-auto.d-block :}
![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/China.png){: .mx-auto.d-block :}
![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/gender.png){: .mx-auto.d-block :}
![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/guangdong.png){: .mx-auto.d-block :}
![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/wordcloud.png){: .mx-auto.d-block :}


### （二）将手机变成电脑终端  

#### 1、基本原理    

##### os 操作系统库  

用于命令输入控制  

#### 2、文件结构    

`./scripts/function/cmd.py`

基本操作函数

#### 3、基本使用方法  

##### （1）将聊天变成命令行：  

```
cmd on
```

之后用户收到的每一句话都会作为命令输入。  

##### （2）退出命令行模式：  

```
cmd off
```

##### （3）杀死所有命令行进程  

```
cmd kill
```

#### 效果：  

![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/1.jpg){: .mx-auto.d-block :}

### （三）聊天机器人   

#### 1、基本原理  

图灵机器人API （[http://www.turingapi.com/](http://www.turingapi.com/)）实现人机交互

#### 2、文件结构  

`./scripts/function/turing.py` 实现相关功能函数

#### 3、基本使用方法

##### （1）启动聊天机器人：  

```
turing on
```

之后当用户在群里被@或者私聊模式下将会对收到的消息进行自动应答。  

##### （2）退出聊天机器人：

```
turing off
```

##### (3）杀死所有聊天机器人进程  

```
turing kill
```

#### 效果：  

![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/2.jpg){: .mx-auto.d-block :}


### （四）目标识别  

#### 1、基本原理

基于yolov3的目标识别神经网络（[https://pjreddie.com/darknet/yolo/](https://pjreddie.com/darknet/yolo/)），实现对收到的图片进行物体目标识别

#### 2、文件结构  

##### （1）./analysis/CV/cv.py  

基本接口函数

##### （2）./analysis/CV/yolo  

yolo神经网络

##### （3）./scripts/function/yolo.py  

对相关函数进行封装

#### 3、基本使用方法  

##### （1）进入目标识别模式  

```
yolo on
```

之后用户受到的图片将会输入神经网络进行处理（限制在处理完一张之前不接受其他输入图片）

##### （2）退出目标识别模式  

```
yolo off
```

##### （3）杀死所有目标识别进程   

```
yolo kill
```

#### 效果：

![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/4.jpg){: .mx-auto.d-block :}
![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/5.jpg){: .mx-auto.d-block :}

### （五）电影链接获取  

#### 1、基本原理  

利用网络爬虫，爬取电影天堂（[https://www.ygdy8.com/](http://www.ygdy8.com/) ）的下载资源

##### （1）requests库  

实现网络通信

##### （2）urllib库  

抓取URL信息

##### （3）re库  

正则表达式

#### 2、文件结构  

`./scripts/function/movie.py`

包含抓取电影资源的函数

#### 3、基本使用方法  

只需要在聊天中输入

```
movie [-电影名]
```

就可以得到结果

#### 效果：

![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/7.jpg){: .mx-auto.d-block :}

### （五）Shazam！  

#### 1、基本原理  

受即将上映的DC超级英雄电影《雷霆沙赞》启发，利用ECCV2018上的一个人脸姿态重建的算法（[https://github.com/YadiraF/PRNet](http://github.com/YadiraF/PRNet)），实现换脸“变身”

#### 2、文件结构  

##### （1）./analysis/CV/cv.py  

基本接口函数

##### （2）./analysis/CV/PRNet  

PRNet神经网络

##### （3）./scripts/function/hero.py  

对相关函数进行封装

#### 3、基本使用方法  

##### （1）进入换脸模式  

```
hero on
```

开启之后，电脑将保存用户收到的图片，当用户输出”shazam“时，最近保存的一张照片将输入神经网络进行处理。

##### （2）退出换脸模式  

```
hero off
```

##### （3）杀死所有换脸进程  

```
hero kill
```

#### 效果：  

![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/6.jpg)

### （六）PC端微信

#### 1、基本原理  

通过GUI实现类似电脑版微信的功能，由于时间关系没有添加过多功能

#### 2、文件结构  

##### （1）./GUI/gui_class.py

定义的类

##### （2）./GUI/gui.py

GUI构建函数

#### 效果：

![](https://chaphlagical.github.io/assets/images/assets-img/WechatRobot/GUI.png){: .mx-auto.d-block :}

## 三、程序结构详解：  

### （一）功能协调  

为将各个功能系统配合起来，又想尽可能减少分支语句的使用，我建了一个文件夹./scripts/function用来存放各个功能实现的函数高级封装，通过文件./scripts/func.py将各函数放在一个字典中，通过主函数中受到的消息关键句进行调用。

### （二）图像的处理  

先保存到特定路径下在进行处理调用，最后发送回微信端。

其他细节处理比较多，便不一一叙述
