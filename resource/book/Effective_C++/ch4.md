## 4. Designs and Declarations

### Item 18：Make interfaces easy to use correctly and hard to use incorrectly

* 考虑一个表现日期的class设计构造函数：

	```c++
	class Date{
	public:
	    Date(int month, int day, int year);
	    ...
	};
	```

	这个接口很容易发生误用：

	```c++
	Date d(30, 3, 1995);	// 无效月份
	Date d(2, 30, 1995);	// 无效天数
	```

	* 优化一：导入外覆类型区别天数、月份和年份

		```c++
		struct Day{
			explicit Day(int d)
		        : val(d) { }
		    int val;
		};
		struct Month{
		    explicit Month(int m)
		        : val(m) { }
		    int val;
		};
		struct Year{
		    explicit Year(int y)
		        : val(y) { }
		    int val;
		};
		class Date{
		    public:
		    Date(const Month& m, const Day& d, const Year& y);
		    ...
		};
		Date d(30, 3, 1995);	// 错误类型
		Date d(Day(30), Month(3), Year(1995));	// 错误类型
		Date d(Month(3), Day(30), Year(1995));	// 正确
		```

	* 优化二：限制类型值

		```c++
		class Month{
		public:
		    static Month Jan() { return Month(1); }
		    static Month Feb() { return Month(2); }
		    ...
		    static Month Dec() { return Month(12); }
		    ...
		private:
		    explicit Month(int m);
		    ...
		};
		Date d(Month::Mar(), Day(30), Year(1995));
		```

	* 优化三：限制类型内什么事可以做，什么事不能做

		* 常见的限制是加上`const`

* 促进正确使用的方法包括：
	* 接口一致性（如STL）
	* 与内置类型的行为兼容
* 防止误用的方法包括：
	* 建立新类型
	* 限制类型上的操作
	* 束缚对象值
	* 消除客户的资源管理责任（智能指针）

### Item 19：Treat class designs as type design

**常见的设计规范**：

* 新type的对象应该如何被创建和销毁？
	* 影响到class的构造函数、析构函数以及内存分配函数和释放函数
* 对象的初始化和对象的赋值该有什么样的差别？
	* 决定构造函数和赋值操作符的行为及其间的差别
* 新type的对象如果被pass-by-value意味着什么？
	* copy构造函数用来定义一个type的pass-by-value该如何实现
* 什么是新type的合法值
	* 对class成员变量而言，通常只有某些数值集是有效的
	* 那些数值集决定了你的class必须维护的约束条件，也决定了你的成员函数（尤其是构造函数、赋值操作符和setter函数）必须进行的错误检查工作
	* 也影响函数抛出的异常以及少数函数异常明细列
* 你的新type需要配合某个继承图系吗？
	* 如果你继承自某些既有的classes，你就受到那些classes的设计束缚，尤其是受到virtual和non-virtual函数的影响
	* 如果你允许其他classes继承你的classes，将会影响你所声明的函数，尤其是析构函数是否为virtual
* 什么样的操作符和函数对此新type而言是合理的？
	* 决定你的class声明哪些函数
* 什么样的标准函数应该被驳回
	* 那些正是你必须声明为`private`的标准函数
* 谁该取用新type的成员？
	* 决定哪些成员为`public`，哪些为`protected`，哪些为`private`
	* 决定哪些classes或functions为`friend`
* 什么是新type的“未声明接口”？
	* 对效率、异常安全性以及资源运用提供保证所需的相应的约束条件
* 你的新type有多么一般化？
	* 若定义了一整个types家族，则应考虑使用template
* 你真的需要一个新的type吗？
	* 应尽可能考虑能否在既有classes基础上新增函数或模板

### Item 20：Prefer pass-by-reference-to-const to pass-by-value