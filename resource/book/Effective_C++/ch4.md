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

* 代码段示例：

	```c++
	class WebBrowser
	{
	public:
	    ...
	    void clearCache();
	    void clearHistory();
	    void removeCookies();
	    ...
	};
	```

	现在需要实现`WebBrowser`的清除功能，可以有两种方法：

	```c++
	class WebBrowser
	{
	public:
	    ...
	    void ClearEverything();	// 清除函数作为类成员函数
	    ...
	};
	
	void clearBrower(WebBrower& wb)
	{
	    wb.clearCache();
	    wb.clearHistory();
	    wb.removeCookies();
	}
	```

	* 事实上，member函数`ClearEverything`的封装性比non-member函数`clearBrower`低
	* 提供non-member函数可允许对`WebBrower`相关机能有较大的包裹弹性，而那最终导致较低的编译依赖度，增加`WebBrower`的可延伸性

* 较大封装性的是non-member non-friend函数，因为它并不增加“能够访问class内的private成分”的函数数量

* class定义式对客户而言是不能扩展的。客户派生的新的classes无法访问base classes中被封装的成员

### Item 24：Declare non-member functions when type conversions should apply to all parameters

* 对有理数类：

	```c++
	class Rational
	{
	public:
	    Rational(int numerator = 0, int denominator = 1); // 允许int-to-Rational隐式转换
	    int numerator() const;
	    int denominator() const;
	private:
	    ...
	};
	```

* 倘若在类内实现`operator*`运算符的重载，即

	```c++
	class Rational
	{
	public:
	    ...
	    const Rational operator*(const Rational& rhs) const;
	};
	```

	此时

	```c++
	Rational oneEnglish(1, 8);
	Rational oneHalf(1, 2);
	Rational result = oneHalf * oneEnglish;	// very good!
	result = result * oneEnglish;			// very good!
	result = oneHalf * 2;					// very good!
	result = 2 * oneHalf;					// wrong!
	```

	要实现最后一句的效果，必须通过：

	```c++
	const Rational temp(2);
	result = oneHalf * temp;
	```

	而对于`explicit`构造函数的`Rational`类，则下面两句均不能通过编译：

	```c++
	result = oneHalf * 2;
	result = 2 * oneHalf;
	```

* 要使得两句均可通过编译，应使用`non-member`函数，允许编译器在每一个实参上执行隐式类型转换

	```c++
	class Rational{
	    ...
	};
	
	const Rational operator*(const Rational& lhs, const Rational& rhs)
	{
	    return Rational(lhs.numerator()*rhs.numerator(),
	                    lhs.denominator()*rhs.denominator());
	}
	Rational oneFourth(1, 4);
	Rational result;
	result = oneFourth * 2;	//
	result = 2 * oneFourth;	// 均可正确编译运行
	```

### Item 25：Consider support for a non-throwing swap

* 标准库实现法

	```c++
	namespace std{
	    template<typename T>
	    void swap(T& a, T& b)
	    {
	        T temp(a);
	        a = b;
	        b = temp;
	    }
	}
	```

* pimpl手法（pointer to implementation）

	```c++
	class WidgetImpl{
	public:
	    ...
	private:
	    int a, b, c;
	    std::vector<double> v;
	    ...
	};
	
	class Widget{
	public:
	    Widget(const Widget& rhs);
	    Widget& operator=(const Widget& rhs)
	    {
	        ...
	        *pImpl = *(rhs.pImpl);	// 详见Item 10, 11, 12
	        ...
	    }
	    ...
	private:
	    WidgetImpl* pImpl;
	};
	```

	* 复制三个Widgets，复制三个WidgetImpl对象，非常缺乏效率

* 模板偏特化

	```c++
	class Widget{
	public:
	    ...
	    void swap(Widget& other)
	    {
	    	using std::swap;
	        swap(pImpl, other.pImpl);
	    }
	    ...
	};
	namespace std{
	    template<>
	    void swap<Widget>(Widget& a, Widget& b)
	    {
	       	a.swap(b);
	    }
	}
	```

* 加入类模板

	```c++
	namespace WidgetStuff{
	    ... ...
	    template<typename T>
	    class WidgetImpl{...};
	
	    template<typename T>
	    class Widget{...};
	    ... ...
	    
	    template<typename T>
	    void swap(Widget<T>& a, Widget<T>& b){ a.swap(b); }
	}
	```

* 总结
	* 当`std::swap`对你的类型效率不高时，提供一个`swap`成员函数，并确定这个函数不抛出异常
	* 如果提供一个`member swap`，也该提供一个`non-member swap`来调用前者。对于`class`也请特化`std::swap`
	* 调用`swap`时应针对`std::swap`使用using声明式，然后调用`swap`且不带任何“命名空间资格修饰”
	* 为“用户定义类型”进行`std template`全特化是好的，但不要在`std`名称空间中加入新东西

