---
bg: "2019-04-28.jpg"
layout: post
title:  "Tensorflow调试技巧"
crawlertitle: "Tensorflow调试技巧"
summary: "Tensorflow调试技巧"
date:   2019-04-28 19:04:15 +0700
categories: posts
tags: ['Tensorflow']
author: Chaf
---



### 1、出现CUDA报错，可以试试

config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))

sess=tf.Session(config=config)