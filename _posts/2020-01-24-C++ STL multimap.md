---
title: C++ STL multimap
tags: C++
article_header:
  type: cover
  image:
    src: /assets/images/C++.jpg
---

<!--more-->

## 简介

multimap 是关联容器的一种，multimap 的每个元素都分为关键字和值两部分，容器中的元素是按关键字排序的，并且允许有多个元素的关键字相同。

注意，不能直接修改 multimap 容器中的关键字。因为 multimap 中的元素是按照关键字排序的，当关键字被修改后，容器并不会自动重新调整顺序，于是容器的有序性就会被破坏，再在其上进行查找等操作就会得到错误的结果。

使用 multimap 必须包含头文件 `<map>`。multimap 的定义如下：

```c++
template < class Key, class T, class Pred = less<Key>, class A = allocator<T> >
class multimap
{
  ...
  typedef pair <const Key, T> value_type;
  ...
};
```

multimap 中的元素都是 pair 模板类的对象。元素的 first 成员变量也叫“关键字”，second 成员变量也叫“值”。multimap 容器中的元素是按关键字从小到大排序的。默认情况下，元素的关键之间用 `less <Key>` 比较大小，也就是用`<`运算符比较大小。**multimap 允许多个元素的关键字相同**。

multimap 中的 value_type 实际上就表示容器中元素的类型。C++允许在类的内部定义类型。

## 成员函数

|                   成员函数或成员函数模板                   |                            作  用                            |
| :--------------------------------------------------------: | :----------------------------------------------------------: |
|              iterator find( const Key & val);              | 在容器中查找关键字等于 val 的元素，返回其迭代器；如果找不到，返回 end() |
|         iterator insert (pair <Key, T> const &p);          |           将 pair 对象 p 插入容器中并返回其迭代器            |
|        void insert(iterator first, iterator last);         |                将区间 [first, last) 插入容器                 |
|                int count( const Key & val);                |             统计有多少个元素的关键字和 val 相等              |
|          iterator lower_bound( const Key & val);           | 查找一个最大的位置 it，使得 [begin( ), it) 中所有的元素的关键字都比 val 小 |
|           iterator upper_bound(const Key & val);           | 查找一个最小的位置 it，使得 [it, end()) 中所有的元素的关键字都比 val 大 |
| pair < iterator, iterator > equal_range (const Key & val); |             同时求得 lower_bound 和 upper_bound              |
|                iterator erase(iterator it);                | 删除 it 指向的元素，返回其后面的元素的迭代器（Visual Studio 2010 中如此，但是在 C++ 标准和 Dev C++ 中，返回值不是这样） |
|       iterator erase(iterator first, iterator last);       | 删除区间 [first, last)，返回 last（Visual Studio 2010 中如此，但是在 C++ 标准和 Dev C++ 中，返回值不是这样） |


multimap 及 map 中的 find 和 count 不用`==`运算符比较两个关键字是否相等。如果`x比y小`和`y比x小`同时为假，就认为 x 和 y 相等。

## 示例

一个学生成绩录入和查询系统接受以下两种输入：
1) Add name id score
2) Query score

name 是一个字符串，其中不包含空格，表示学生姓名。id 是一个整数，表示学号。score 是一个整数，表示分数。学号不会重复，分数和姓名都可能重复。

两种输入交替出现。

- 第一种输入表示要添加一个学生的信息，碰到这种输入，就记下学生的姓名、id 和分数。
- 第二种输入表示要查询分数为 score 的学生的信息，碰到这种输入，就输出已有记录中分数比查询分数低的最高分获得者的姓名、学号和分数。如果有多个学生满足条件，则输出学号最大的学生的信息。如果找不到满足条件的学生，则输出“Nobody”。

```c++
#include <iostream>
#include <map>  //使用multimap需要包含此头文件
#include <string>
using namespace std;
class CStudent
{
public:
    struct CInfo  //类的内部还可以定义类
    {
        int id;
        string name;
    };
    int score;
    CInfo info;  //学生的其他信息
};
typedef multimap <int, CStudent::CInfo> MAP_STD;
int main()
{
    MAP_STD mp;
    CStudent st;
    string cmd;
    while (cin >> cmd) {
        if (cmd == "Add") {
            cin >> st.info.name >> st.info.id >> st.score;
            mp.insert(MAP_STD::value_type(st.score, st.info));
        }
        else if (cmd == "Query") {
            int score;
            cin >> score;
            MAP_STD::iterator p = mp.lower_bound(score);
            if (p != mp.begin()) {
                --p;
                score = p->first;  //比要查询分数低的最高分
                MAP_STD::iterator maxp = p;
                int maxId = p->second.id;
                for (; p != mp.begin() && p->first == score; --p) {
                    //遍历所有成绩和score相等的学生
                    if (p->second.id > maxId) {
                        maxp = p;
                        maxId = p->second.id;
                    }
                }
                if (p->first == score) { //如果上面的循环因为 p == mp.begin()
                                         //而终止，则p指向的元素还要处理
                    if (p->second.id > maxId) {
                        maxp = p;
                        maxId = p->second.id;
                    }
                }
                cout << maxp->second.name << " " << maxp->second.id << " "
                    << maxp->first << endl;
            }
            else  //lower_bound 的结果就是 begin，说明没有分数比查询分数低
                cout << "Nobody" << endl;
        }
    }
    return 0;
}
```

