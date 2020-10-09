## 3. Resource Management

### Item 13：Use objects to manage resources

* 以对象管理资源的两个关键想法
	* 获得资源后立即放入管理对象
		* 资源取得时机便是初始化时机（Resource Acquisition Is Initialization；RAII）
	* 管理对象运用析构函数确保资源被释放
* 智能指针简介
	* `auto_ptr`
		* 被销毁时会自动删除它所指之物
		* 若通过`copy`构造函数或`copy assignment`操作符复制它们，它们将变成`null`，而复制得到的指针取得资源的唯一所有权
		* 受`auto_ptrs`管理的资源必须绝对没有一个以上的`auto_ptr`同时指向它
		* 现代C++中常用`unique_ptr`代替`auto_ptr`
	* `shared_ptr`
		* 属于引用计数型智能指针（Reference-counting smart pointer;RCSP）
		* 持续追踪共有多少对象指向某笔资源，并在无人指向它时自动删除该资源

* 智能指针`auto_ptr`和`tr1::shared_ptr`的析构函数内进行的删除操作为`delete`，因此不建议在动态分配得到的数组上使用智能指针

### Item 14：Think carefully about copying behavior in resource-managing classes

* 复制RAII对象必须一并复制它所管理的资源，所以资源的`copy`行为决定RAII的`copy`行为

* 常见的RAII`copy`行为有：

	1. 禁止复制

		* 将`copy`操作声明为`private`

	2. 对底层资源使用“引用计数”（`shared_ptr`）

		* 保有资源直到其最后一个使用者被销毁，该情况下复制RAII对象，其被引用数将递增
		* `shared_ptr`允许指定删除器，引用次数为0时将自动调用删除器，如：

		```c++
		class Lock{
		public:
		    explicit Lock(Mutex* pm)
		        : mutexPtr(pm, unlock)	// 指定unlock函数作为删除器
		        {
		            lock(mutexPtr.get());
		        }
		private:
		    std::tr1::shared_ptr<Mutex> mutexPtr;
		}
		```

	3. 复制底部资源

		* 复制资源管理对象时，应该同时复制其所包覆的资源，即进行深度拷贝

	4. 转移底部资源的所有权（`auto_ptr`）

		* 希望确保永远只有一个RAII对象指向一个原始资源
		* 当RAII对象被复制时，资源的拥有权从被复制对象转移到目标对象

### Item 15：在资源管理类中提供对原始资源的访问

* 往往是接口需要

* 显式转换与隐式转换

	```c++
	FontHandle getFont();				// C API
	void releaseFont(FontHandle fh);	// C API
	class Font{
	public:
	    explicit Font(FontHandle fh)
	        :f(fh)
	        {}
	    ~Font(){releaseFont(f);}
	private:
	    FontHandle f;
	};
	```

	* 显式转换

		```c++
		class Font{
		public:
		    ...
		    FontHandle get() const {return f;}
		    ...
		};
		```

		每次使用时必须调用`get`

		```c++
		void changeFontSize(FontHandle f, int newSize);
		Font f(getFont());
		int newFontSize;
		...
		changeFontSize(f.get(),newFontSize);
		```

		这种做法暴露了原始资源，增加资源泄露的风险

	* 隐式转换

		```c++
		class Font{
		public:
		    ...
		    operator FontHandle() const
		    {return f;}
		    ...
		};
		```

		这种方法客户端调用更加自然

		```c++
		Font f(getFont());
		int newFontSize;
		...
		changeFontSize(f, newFontSize);
		```

		隐式转换也会增加发生错误的机会，比如客户可能在需要`Font`的时候意外创建一个`FontHandle`

		```c++
		Font f1(getFont());
		...
		FontHandle f2=f1;
		```

	* 一般而言，显式转换比较安全，而隐式转换更加客户友好

### Item 16：Use the same form in corresponding uses of new and delete

* 使用`new`时，有两件事发生

	* 内存被分配出来
	* 针对此内存会有一个或更多构造函数被调用

* 使用`delete`时，有两件事发生

	* 针对此内存会有一个或更多析构函数被调用
	* 内存被释放

* 数组的删除

	* 和单一对象的内存布局不同，数组所用内存通常还包括“数组大小”的记录，以便删除函数直到需要调用多少次析构函数
	* 对于数组的删除，应当使用`delete[]`

* 使用了`typedef`

	```c++
	typedef std::string AddressLines[4];
	std::string* pal = new AddressLines;
	delete pal;		// 行为未定义
	deletep[] pal;	// 正确
	```

	为减少错误的产生，尽量不要对数组形式做`typedef`操作

### Item 17：Stored newed objects in smart pointers in standalone statement

* 智能指针构造函数需要一个原始指针，但该构造函数是个`explicit`构造函数，无法进行隐式转换

	```c++
	int priority();
	void processWidget(std::tr1::shared_ptr<Widget> pw, int priority);
	```

	考虑调用

	```c++
	processWidget(new Widget, priority());
	```

	将不能通过编译，欲使程序正常编译，应显式调用：

	```c++
	processWidget(std::tr1::shared_ptr<Widget>(new Widget), priority());
	```

* `std::tr1::shared_ptr<Widget>(new Widget)`调用过程：

	1. 执行`new Widget`表达式
	2. 调用`std::tr1::shared_ptr`构造函数

* 调用`processWidget`前编译器的工作：

	* 调用`priority`

	* 执行`new Widget`表达式

	* 调用`std::tr1::shared_ptr`构造函数

	C++完成上述任务的顺序弹性很大，不过可以肯定的是`new Widget`一定在`std::tr1::shared_ptr`构造函数被调用前执行。

	倘若调用`priority`在其他两个操作中间，此时如果`priority`调用异常，`new Widget`得到的指针将无法送到智能指针处，导致资源泄露

* 科学的方法是使用分离语句

	```c++
	std::tr1::shared_ptr<Widget> pw(new Widget);
	processWidget(pw, priority());
	```

	

