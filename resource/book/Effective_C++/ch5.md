## Implementations

### Item 26：Postpone variable definitions as long as possible

* 只要定义了一个变量而其类型带有一个构造函数或析构函数，那么当程序的控制流到达这个变量定义式时，就得承受构造成本；当这个变量离开作用域时，便得承受析构成本。即使这个变量最终并未被使用，仍需耗费这些成本。

* 过早定义变量的一个例子：

	```c++
	std::string encryptPassword(const std::string& password)
	{
	    using namespace std;
	    string encrypted;
	    if(password.length()<MinimumPasswordLength){
	        throw logic_error("Password is too short");
	    }
	    ...
	    return encrypted;
	}
	```

	* 如果函数`encryptPassword`丢出异常，仍得付出`encrypted`的构造成本和析构成本

* 延后变量的定义

	```c++
	std::string encryptPassword(const std::string& password)
	{
	    ...
	    std::string encrypted(password);
	    
	    encrypt(encrypted);
	    return encrypted;
	}
	```

	* 延后变量定义直到非得使用该变量的前一刻为止，甚至应尝试延后到能够给它初值实参为止
	* 避免构造/析构非必要对象，避免无意义的default构造行为

* 循环情况

	```c++
	//	方法A：定义于循环外
	Widget w;
	for(int i=0;i<n;i++)
	{
	    w=...;
	    ...
	}
	
	//	方法B：定义于循环内
	for(int i=0;i<n;i++)
	{
	    Widget w...;
	    ...
	}
	```

	* 方法A：1个构造函数+1个析构函数+n个赋值操作
	* 方法B：n个构造函数+n个析构函数
	* 除非你知道赋值成本比“析构+构造”低、你正在处理代码中效率高度敏感的部分，否则应该使用做法B

### Item 27：Minimize casting

* 旧式转型
	* `(T)expression`：C-style
	* `T(expression)`：函数风格
* 新式转型
	* `const_cast<T>(expression)`
		* `const_cast`通常用来将对象的常量性移除，也是唯一具有此能力的C++-style转型操作符
	* `dynamic_cast<T>(expression)`
		* `dynamic_cast`主要用来执行“安全向下转型”，用来决定某对象是否归属继承体系中的某个类型
		* 唯一无法由旧式语法执行的动作，也是唯一可能耗费重大运行成本的转型动作
	* `reinterpret_cast<T>(expression)`
		* ``reinterpret_cast`意图执行低级转型，实际动作可能取决于编译器，这也表示它不可移植
	* `static_cast<T>(expression)`
		* `static_cast`用来强迫隐式转换
* 新式转型相较旧式转型的好处
	* 容易在代码中被辨识出来，简化“找出类型系统在哪个地点被破坏”的过程
	* 各转型动作的目标越窄化，编译器越可能诊断出错误的运用
* 任何一种类型转换往往真的令编译器编译出运行期间执行的码，而不是简单地将一种类型视为另外一种类型
	* 对象地布局方式和他们的地址计算方式随编译器的不同而不同，意味着“由于知道对象如何布局”而设计的转型，在某一平台上行得通，在其他平台并不一定行得通

* 类继承的转型问题

	```c++
	class Window{
	public:
	    virtual void onResize() {...}
	    ...
	};
	class SpecialWindow: public Window{
	public:
	    virtual void Resize(){
	        static_cast<Window>(*this).onResize();
	        ...
	    }
	    ...
	};
	```

	* 上述代码并非是在当前对象上调用`Window::onResize`之后在该对象上执行`SpecialWindow`专属动作
	* 而是在当前对象的`base class`成分的副本上调用`Window::onResize`，任何在当前对象身上执行`SpecialWindow`专属动作

	正确的写法应该是：

	```c++
	class SpecialWindow: public Window{
	public:
	    virtual void Resize(){
	        Window::onResize();
	        ...
	    }
	    ...
	};
	```

* `dynamic_cast`的避免

	* `dynamic_cast`的应用场景：你想在一个你认为`derived class`对象身上执行`derived class`操作函数，但你的手上只有一个指向`base`的pointer或reference，只能靠它们来解决问题

	* 方法一：使用容器并在其中存储直接指向`derived class `对象的指针，如此便消除了通过base class接口处理对象的需要

		```c++
		class Window{...}
		class SpecialWindow: public Window{
		public:
		    void blink();
		    ...
		};
		
		// dynamic_cast实现方法
		typedef std::vector<std::trl::shared_ptr<Window>> VPW;
		VPW winPtrs;
		...
		for(VPW::iterator iter=winPtrs.begin();iter!=winPtrs.end();++iter)
		{
		    if(SpecialWindow* psw=dynamic_cast<SpecialWindow*>(iter->get()))
		        psw->blink();
		}
		// 改进实现方法
		typedef std::vector<std::trl::shared_ptr<SpecialWindow>> VPSW;
		VPSW winPtrs;
		...
		for(VPSW::iterator iter=winPtrs.begin();iter!=winPtrs.end();++iter)
		{
		    (*iter)->blink();
		}
		```

		* 该方法使你无法在同一个容器内存储指针”指向所以可能的Window派生类“。处理多中Window类型需要多各容器，它们都必须具备类型安全性

	* 方法二：通过base class接口处理所有可能的Window派生类，即在base class内提供virtual函数做你想对各个window派生类做的事

		```c++
		class Window{
		public:
		    virtual void blink() { }
		    ...
		};
		class SpecialWindow: public Window{
		public:
		    virtual void blink() { ... };
		    ...
		};
		typedef std::vector<std::trl::shared_ptr<Window>> VPW;
		VPW winPtrs;
		...
		for(VPW::iterator iter=winPtrs.begin();iter!=winPtrs.end();++iter)
		    (*iter)->blink();
		```

### Item 28：Avoid returning "handles" to object internals

* 考虑矩形类：

	```c++
	class Point{
	public:
	    Point(int x, int y);
	    ...
	    void setX(int newVal);
	    void setY(int newVal);
	    ...
	};
	struct RectData{
	    Point ulhc;
	    Point lrhc;
	};
	class Rectangle{
	    ...
	private:
	    std::trl::shared_ptr<RectData> pData;
	};
	```

* handles： Reference、指针和迭代器

	* 降低对象封装性

	* 可能导致虽然调用`const`成员函数却造成对象状态被更改

		例如：

		```c++
		class Rectangle{
		public:
		    ...
		    Point& upperleft() const {return pData->ulhc;}
		    Point& lowerright() const {return pData->lrhc;}
		    ...
		};
		
		Point coord1(0, 0);
		Point coord2(100, 100);
		const Rectangle rec(coord1, coord2);
		
		rec.upperLeft().setX(50);	// 将会改变rec，而定义使用了const
		```

		该问题的解决方法是返回const reference：

		```c++
		class Rectangle{
		public:
		    ...
		    const Point& upperleft() const {return pData->ulhc;}
		    const Point& lowerright() const {return pData->lrhc;}
		    ...
		};
		```

* 返回代表对象内部的handles可能导致空悬的句柄（dangling handles）：这种handles所指的东西不复存在

	例如：

	```c++
	class GUIObject {...};
	const Rectangle boundingBox(const GUIObject& obj);
	GUIObject* pgo;
	...
	const Point* pUpperLeft = &(boundingBox(*pgo).upperLeft());
	```

	* 这里`boundingBox`生成一个临时变量，在语句结束后将自动被销毁，最后`pUpperLeft`得到将是一个空悬、虚吊的handles

* 返回`handles`的特例：重载`operator[]`以获取数据等