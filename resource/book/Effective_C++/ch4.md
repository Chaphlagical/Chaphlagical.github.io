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

* 缺省情况下C++以pass-by-value方式传递对象至函数。函数参数都是以实际实参的复件为初值，而调用端所获得的亦是函数返回值的一个复件，这些复件由对象的copy构造函数产生，这可能使得pass-by-value成为昂贵的操作

	举例：有两个类定义如下

	```c++
	class Person{
	public:
	    Person();
	    virtual ~Person();
	    ...
	private:
	    std::string name;
	    std::string address;
	};
	class Student: public Person{
	public:
	    Student();
	    ~Student();
	    ...
	private:
	    std::string schoolName;
	    std::string schoolAddress;
	};
	```

	考虑调用

	```c++
	bool validateStudent(Student s);
	Student plato;
	bool platoIsOK = validateStudent(plato);
	```

	* 以by value方式传递一个Student对象会导致调用一次Student copy构造函数、一次Person copy构造函数、四次string copy构造函数
	* 当函数内哪个Student复件被销毁，每一个构造函数调用动作都需要一个对应的析构函数调用动作
	* 以by value方式传递的总成本为六次构造函数和六次析构函数

* pass by reference-to-const

	```c++
	bool validateStudent(const Student& s);
	```

	* 没有任何构造函数和析构函数被调用，因为没有任何新对象被创建
	* `const`的必要性：防止函数对引用进行修改
	* 避免对象切割问题：当一个derived class对象以by value方式传递并被视为一个base class对象，base class的copy构造函数将被调用，而造成derived class的特化性质被切割掉，仅仅留下一个base class对象

* 不适合使用pass by reference-to-const的应用场景

	* 内置类型、STL迭代器和函数对象
	* references往往以指针实现出来，因此pass-by-reference通常意味真正传递的指针
	* 如果对象属于内置类型（或STL迭代器、函数对象），pass by value往往比pass by reference的效率高些

### Item 21：Prefer pass-by-reference-to -const to pass-by-value

* 考虑代码段

	```c++
	class Rational
	{
	public:
	    Rational(int numerator = 0, int denominator = 1);
	    ...
	private:
	    int n,d;
	friend
	    const Rational& operator*(const Rational& lhs, const Rational& rhs);
	}
	```

	`opertaor*`的实现，需要返回一个reference指向的Rational对象，方法以下：

	1. 在stack空间上创建local变量

		```c++
		const Rational& operator*(const Rational& lhs, const Rational& rhs)
		{
		    Rational result(lhs.n * rhs.n, lhs.d * rhs.d);
		    return result;
		}
		```

		* 返回的是local变量，而local变量将在函数结束时被销毁，将带来意外风险

	2. 在heap空间上创建对象，并返回reference指向它

		```c++
		const Rational& operator*(const Rational& lhs, const Rational& rhs)
		{
		    Rational* result = new Rational(lhs.n * rhs.n, lhs.d * rhs.d);
		    return *result;
		}
		```

		* `new`之后的对象没能进行`delete`，将带来内存泄漏

	3. 返回reference指向一个被定义于函数内部的`static Rational`对象

		```
		const Rational& operator*(const Rational& lhs, const Rational& rhs)
		{
		    static Rational result;
		    result = ...;
		    return *result;
		}
		```

		* 多线程安全

		* 其他错误：

			```c++
			bool operator==(const Rational& lhs, const Rational& rhs);
			Rational a, b, c, d;
			...
			if((a * b) == (c * d))
			{
			    ...
			}
			else
			{
			    ...
			}
			```

			* 这里由于`operator*`返回`static Rational`的reference，因此函数总是看到它们的现值，故`operator==`判断总是为`true`

* 正确的写法应该是：

	```c++
	inline const Rational lhs, const Rational& rhs)
	{
	    return Rational(lhs.n * rhs.n, lhs.d * rhs.d);
	}
	```

	而不应返回reference

### Item 22：Declare data members private

* 语法一致性

	* 如果成员变量不是`public`，客户唯一能够访问对象的办法就是通过成员函数

* 对成员变量的处理有更加精确的控制，例如：

	```c++
	class AccessLevels{
	public:
	    ...
	    int getReadOnly() const { return readOnly; }
	    void SetReadWrite(int value) { readWrite = value; }
	    int getReadWrite() const { return readWrite; }
	    void setWriteOnly(int value) { writeOnly = value; }
	private:
	    int noAccess;	// 不操作
	    int readOnly;	// 只读
	    int readWrite;	// 读写
	    int writeOnly;	// 只写
	};
	```

* 封装
	* 对客户隐藏成员变量（封装），可以确保class的约束条件总是会获得维护，因为只有成员函数可以影响它们
	* `public`意味着不封装
	* `protected`成员变量同样缺乏封装性
	* 从封装角度看，只有两种访问权限：`private`和其他

### Item 23：Prefer non-member non-friend functions to member functions

