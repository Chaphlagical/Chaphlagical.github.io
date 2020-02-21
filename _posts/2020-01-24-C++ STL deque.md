---
title: C++ STL deque
tags: C++
article_header:
  type: cover
  image:
    src: /assets/images/C++.jpg
---

<!--more-->

deque 也是顺序容器的一种，同时也是一个可变长数组。要使用 deque，需要包含头文件 deque。所有适用于 vector 的操作都适用于 deque。

deque 和 vector有很多类似的地方。在 deque 中，随机存取任何元素都能在常数时间内完成（但慢于vector）。它相比于 vector 的优点是，vector 在头部删除或添加元素的速度很慢，在尾部添加元素的性能较好，而 deque 在头尾增删元素都具有较好的性能（大多数情况下都能在常数时间内完成）。它有两种 vector 没有的成员函数：

```c++
void push_front (const T & val); //将 val 插入容器的头部
void pop_front(); //删除容器头部的元素
```