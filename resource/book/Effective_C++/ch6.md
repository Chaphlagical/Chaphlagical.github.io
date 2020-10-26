## Inheritance and Object-Oriented Design

### Item 32: Make Sure public inheritance models "is-a"

* `public inheritance`（公开继承）意味着“is-a”（是一种）的关系

* 如果令class D以public形式继承class B，便是告知C++编译器每个类型为D的对象同时也是一个类型为B的对象，反之不成立

* 考虑public继承

	```c++
	class Person{...};
	class student: public Person{...};
	```

	* 每个学生都是人，但并非每个人都是学生

	* 在C++中，任何函数如果期望获得一个类型为Person（或pointer-to-Person或reference-to-Person）的实参，也都愿意接受一个Student对象（或pointer-to-Student或reference-to-Student）

		```c++
		void eat(const Person& p);		// all person will eat
		void study(const Student& s);	// only students study
		Person p;
		Student s;
		eat(p);							// √
		eat(s);							// √
		study(p);						// ×， person is not student
		study(s);						// √
		```

* “is-a”并非唯一存在于classes之间的关系，另外两个常见的关系是“has-a”（有一个）和“is-implemented-in-terms-of”（根据某物实现出）

### Item 33: Avoid hiding inherited names

* 遮掩名称：作用域相关

	```c++
	int x;	// global variable
	void someFunc()
	{
	    double x;	// local variable
	    std::cin>>x;
	}
	```

	* 当编译器处于`someFunc`的作用域内并遭受名称`x`时，它在local作用域内查找是否有什么东西带着这个名称。如果找到了就不再找其他作用域

* 遮掩继承：derived class作用域被嵌套在base class作用域内

	```c++
	class Base{
	private:
	    int x;
	public:
	    virtual void mf1() = 0;
	    virtual void mf2();
	    void mf3();
	    ...
	};
	class Derived: public Base{
	public:
	    virtual void mf1();
	    void mf4();
	    ...
	};
	```

	* 假设derived class内的`mf4`的实现如下：

		```c++
		void Derived::mf4()
		{
		    ...
		    mf2();
		    ...
		}
		```

		* 查找顺序：local作用域 → class Derived作用域 → base class作用域 → 含Base的namespace → global作用域

	* 重载

		```c++
		class Base{
		private:
		    int x;
		public:
		    virtual void mf1() = 0;
		    virtual void mf1(int);
		    virtual void mf2();
		    void mf3();
		    void mf3(double);
		    ...
		};
		class Derived: public Base{
		public:
		    virtual void mf1();
		    void mf3();
		    void mf4();
		    ...
		};
		```

		* base class内所有名为`mf1`和`mf3`的函数都被derived class内的`mf1`和`mf3`函数遮掩掉。从名称查找观点看，`Base::mf1`和`Base::mf3`不再被Derived继承

			```c++
			Derived d;
			int x;
			...
			d.mf1();	// √ 调用Derived::mf1
			d.mf1(x);	// × Derived::mf1遮掩了Base::mf1
			d.mf2();	// √ 调用Base::mf2
			d.mf3();	// √ 调用Derived::mf3
			d.mf3(x);	// × Derived::mf3遮掩了Base::mf3
			```

		* 上述规则对base classes和derived classes内的函数有不同的参数类型也适用，而且无论函数是virtual还是non-virtual也适用

		* 若继承base class并加上重载函数，有希望重新定义或覆写其中一部分，则必须为那些原本会被遮掩的每个名称引入一个`using`声明式，否则某些你希望继承的名称会被遮掩

			```c++
			class Base{
			private:
			    int x;
			public:
			    virtual void mf1() = 0;
			    virtual void mf1(int);
			    virtual void mf2();
			    void mf3();
			    void mf3(double);
			    ...
			};
			class Derived: public Base{
			public:
			    using Base::mf1;
			    using Base::mf3;
			    virtual void mf1();
			    void mf3();
			    void mf4();
			    ...
			};
			```

* 继承base classes的部分函数

	* 在public继承下是不可能出现的，因为违反了“is-a”关系
	* 在private继承下是有意义的，通过转交函数实现

	```c++
	class Base{
	public:
	    virtual void mf1() = 0;
	    virtual void mf1(int);
	    ...
	};
	class Derived: private Base{
	public:
	    virtual void mf1()
	    {Base::mf1();}	// inline转交函数
	    ...
	};
	...
	Derived d;
	int x;
	d.mf1();	// √ 调用Derived::mf1
	d.mf1(x);	// × Base::mf1被遮掩了
	```

### Item 34: Differentiate

