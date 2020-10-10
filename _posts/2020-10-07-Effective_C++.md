---
layout: post
title: Effective C++ Note
subtitle: 《Effecitve C++》3ed学习笔记（持续更新）
thumbnail-img: ""
cover-img: "/assets/images/cover-img/Effective_C++.jpg"
comments: true
tags: [Note]
readtime: true
---

《Effective C++》阅读笔记

>英文书名：《Effective C++ Third Edition: 55 Specific Ways to Improve Your Programs and Designs》
>
>中文书名：《高效C++第三版：改善程序与设计的55个具体做法》
>
>作者：[Scott Meyers](http://scottmeyers.blogspot.com/)
>
>电子书下载地址：[Link](https://chaphlagical.github.io/resource/book/Effective_C++/Efffective_C++.pdf)

**学习笔记**

1. [让自己习惯C++（Accustoming Yourself to C++）](https://chaphlagical.github.io/resource/book/Effective_C++/ch1.html)
	* **Item 1**：视C++为一个语言联邦（View C++ as a federation of languages）
	* **Item 2**：尽量以`const`，`enum`，`inline`替换`#define` （Prefer consts, enums, and inlines to #define）
	* **Item 3**：尽可能使用`const` （Use const whenever possible）
	* **Item 4**：确定对象被使用前已先被初始化（Make sure that objects are initialized before you're used）
2. [构造/析构/赋值运算（Constructors, Destructors, and Assignment Operators）](https://chaphlagical.github.io/resource/book/Effective_C++/ch2.html)
	* **Item 5**：了解C++默认编写并调用哪些函数（Know what functions C++ silently writes and calls）
	* **Item 6**：若不想使用编译器自动生成的函数，就应该明确拒绝（Explicitly disallow the use of compiler-generated functions you do not want）
	* **Item 7**：为多态声明`virtual`析构函数（Declare destructors virtual in polymorphic base classes）
	* **Item 8**：别让异常逃离析构函数（Prevent exceptions from leaving destructors）
	* **Item 9**：绝不在构造和析构过程中调用`virtual`函数（Never call virtual functions during construction or destruction）
	* **Item 10**：令`operator=`返回一个`*this`的引用（Have assignment operators return a reference to `*this`）
	* **Item 11**：在`operator=`中处理“自我赋值”（Handle assignment to self in `operator=`）
	* **Item 12**：复制对象时勿忘其每一个成分（Copy all parts of an object）
3. [资源管理（Resource Management）](https://chaphlagical.github.io/resource/book/Effective_C++/ch3.html)
	* **Item 13**：以对象管理资源（Use objects to manage resources）
	* **Item 14**：在资源管理类中小心`copy`行为（Think carefully about copying behavior in resource-managing classes）
	* **Item 15**：在资源管理类中提供对原始资源的访问（Provide access to raw resources in resource-managing classes）
	* **Item 16**：成对使用`new`和`delete`时要采取相同形式（Use the same form in corresponding uses of new and delete）
	* **Item 17**：以独立语句将`newed`对象置入智能指针（Stored newed objects in smart pointers in standalone statements）
4. [设计与声明（Designs and Declarations）](https://chaphlagical.github.io/resource/book/Effective_C++/ch4.html)
	* **Item 18**：让接口容易被正确使用，不易被误用（Make interfaces easy to use correctly and hard to use incorrectly）
	* **Item 19**：设计class犹如设计type（Treat class design as type design）
	* **Item 20**：宁以pass-by-reference-to-const替换pass-by-value（Prefer pass-by-reference-to-const to pass-by-value）
	* **Item 21**：必须返回对象时，别妄想返回其reference（Don't try to return a reference when you must return an object）
	* **Item 22**：将成员变量声明为`private`（Declare data members private）
	* **Item 23**：宁以non-member、non-friend替换member函数（Prefer non-member non-friend functions to member functions）
	* **Item 24**：若所有参数皆需类型转换，请为此采用non-member函数（Declare non-member functions when type conversions should apply to all parameters）
	* **Item 25**：考虑写一个不抛出异常的`swap`函数（Consider support for a non-throwing swap）
5. 实现（Implementations）
6. 继承与面向对象设计（Inheritance and Object-Oriented Design）
7. 模板与泛型编程（Templates and Generic Programming）
8. 定制new和delete（Customizing new and delete）
9. 杂项讨论（Miscellany）