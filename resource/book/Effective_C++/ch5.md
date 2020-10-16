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

### Item 29：Strive for exception-safe code

* 

* 举例一个希望用于多线程环境的GUI菜单类

	```c++
	class PrettyMenu{
	public:
	    ...
	    void changeBackground(std::istream& imgSrc);
	    ...
	private:
	    Mutex mutex;		// 互斥器
	    Image* bgImage;		// 目前背景图片
	    int imageChanges;	// 背景图片被改变的次数
	};
	```

	`changeBackground`函数的一个实现：

	```c++
	void PrettyMenu::changeBackground(std::istream& imgSrc)
	{
	    lock(&mutex);				// 获取互斥器
	    delete bgImage;				// 删除旧背景
	    ++imageChanges;				// 修改图片变更次数
	    bgImage=new Image(imgSrc);	// 使用新背景
	    unlock(&mutex);				// 释放互斥锁
	}
	```

	从“异常安全性”上看，这个函数的设计很糟糕

* 异常安全性函数的满足条件：

	1. 不泄露任何资源
		* 对上述`changeBackground`函数的实现，若`new Image(imgSrc)`发生异常，则`unlock`永远不会被调用，互斥器永远被把持住
	2. 不允许数据败坏
		* 若`new Image(imgSrc)`抛出异常，`bgImage`将指向一个被删除的对象，`imageChanges`也被累加，而事实上并没有新的图像加载成功

* 此处资源泄露问题可以使用资源管理类解决

	```c++
	void PrettyMenu::changeBackground(std::istream& imgSrc)
	{
	    lock m1(&mutex);			// 获取互斥器，并确保未来销毁
	    delete bgImage;				// 删除旧背景
	    ++imageChanges;				// 修改图片变更次数
	    bgImage=new Image(imgSrc);	// 使用新背景
	}
	```

* 异常安全函数提供三个保证

	1. 基本承诺：如果异常被抛出，程序内的任何事物仍然保持在有效状态下。没有任何对象或数据结构会因此而败坏，所有对象均处于一种内部前后一致的状态。然而程序的现实状态恐怕不可预料。例如，可以编写`changeBackground`函数异常抛出时，`PrettyMenu`可以继续拥有背景图片，或者令它拥有某个缺省的背景图像，但客户无法预期是哪一种情况

	2. 强烈保证：如果异常被抛出，程序状态不改变。调用这样的函数需要有这样的认知：如果函数成功，就是完全成功，如果函数失败，程序会回退到函数调用之前的状态

	3. 不抛掷保证：承诺绝不抛出异常，因为它们总能完成它们原先承诺的功能。作用于内置类型身上的所有操作都提供`nothrow`保证。例如

		```c++
		int doSomethin() throw();
		```

		并不是说明`doSomething`不会抛出异常，而是说如果`doSomething`抛出异常，将是严重错误，会有意想不到的函数被调用。同时`doSomething`也没有提供任何异常保证

* 对`changeBackground`函数安全性的优化

	1. 改变`PrettyMenu`的`bgImage`成员变量类型，从一个类型为`Image*`的内置指针改为一个智能指针
	2. 重新排列`changeBackground`函数内语句次序，使得在更换图像之后才累加`imageChanges`

	```c++
	class PrettyMenu{
	    ...
	    std::tr1::shared_ptr<Image> bgImage;
	    ...
	};
	void PrettyMenu::changeBackground(std::istream& imgSrc)
	{
	    Lock m1(&mutex);
	    bgImage.reset(new Image(imgSrc));
	    ++imageChanges;
	}
	```

	* 如果`Image`构造函数抛出异常，有可能输入流的读取记号已被移走，这样的搬移对程序的其余部分是一种可见的状态改变，在保证`changeBackground`提供强烈保证前提下，可以使用下述方法解决这一问题
		* copy and swap策略：为打算修改的对象做出一份副本，然后在那副本身上做一切必要修改。若有任何修改动作抛出异常，原对象仍保持未改变状态。待所有改变都成功后，再将修改过的那个副本和原对象在一个不抛出异常的操作中置换
		* 实现：将所有“隶属对象的数据”从原对象放进另外一个对象内，如何赋予原对象一个指针，指向那个所谓的实现对象（即副本）。该手法常称为pimpl idiom

	```c++
	struct PMImpl{
	    std::tr1::shared_ptr<Image> bgImage;
	    int imageChanges;
	};
	class PrettyMenu{
	    ...
	private:
	    Mutex mutex;
	    std::tr1::shared_ptr<PMImpl> pImpl;
	};
	void PrettyMenu::changeBackground(std::istream& imgSrc)
	{
	    using std::swap;
	    Lock ml(&mutex);
	    std::tr1::shared_ptr<PMImpl> pNew(new PMImpl(*pImpl));
	    pNew->bgImage.reset(new Image(imgSrc));
	    ++pNew->imageChanges;
	    swap(pImpl, pNew);
	}
	```

	* copy-and-swap策略是对对象状态做出全有或全无改变的一个很好方法，但一般而言它并不保证整个函数具有强烈的异常安全性，考虑代码：

		```c++
		void someFunc()
		{
		    ...
		    f1();
		    f2();
		    ...
		}
		```

		* 如果`f1`或`f2`的异常安全性比“强烈保证”低，就很难让`someFunc`成为“强烈异常安全”。例如，假设`f1`只提供基本保证，则为了使`someFunc`提供强烈保证，必须写出代码获得调用`f1`之前的整个程序状态、捕捉`f1`所有可能异常、然后恢复原状态
		* 如果`f1`和`f2`都是“强烈异常安全”，如果`f1`圆满结束，程序状态在任何方面都可能有所改变，因此如果`f2`随后抛出异常，程序状态和`someFunc`被调用前并不相同，甚至当`f2`没有改变东西时也是如此

	* 函数提供的“异常安全保证”通常最高只等于其所调用之各个函数的“异常安全保证”中的最弱者

### Item 30：Understand the ins and outs of inlining

* 在一台内存有限的机器上，过度热衷`inlining`会造成程序体积太大（对可用空间而言）。即使拥有虚内存，`inline`造成的代码膨胀亦会导致额外的换页行为，降低指令高速缓存装置的击中率，以及伴随这些而来的效率损失

* 如果`inline`函数本体很小，编译器针对函数本体所产生的码可能比针对函数调用所产生的码更小。这样的话，将函数`inlining`确实可能导致较小的目标码和较高的指令高速缓存装置击中率

* `inline`只是对编译器的一个申请，不是强制命令

	* 可以明确提出

		```c++
		template<typename T>
		inline const T& std::max(const T& a, const T&b)
		{
		    return a<b? b : a;
		}
		```

	* 也可以隐喻方式提出，即将函数定义于class定义式内

		```c++
		class Person{
		public:
		    ...
		    int age() const {return theAge;}
		    ...
		private:
		    int theAge;
		};
		```

* `inline`函数通常一定被置于头文件内，因为大多数建置环境在编译过程中进行`inlining`，而为了将一个“函数调用”替换为“被调用函数的本体”，编译器必须知道那个函数长什么样。`inlining`在大多数C++程序中是编译期行为

* `template`通常也被置于头文件内，因为它一旦被使用，编译器为了将它具现化，需要知道它长什么样。而`template`与`inlining`无关，所以不应该将所有的`tempalte function`声明为`inline`

* 所有对`virtual`函数的调用也都会使`inlining`落空，因为`virtual`意味着“等待，直到运行期才确定调用哪个函数”，而`inline`意味着“执行前，先将调用动作替换为被调用函数的本体”

* 一个表面看似`inline`的函数是否真的能`inline`取决于建置环境，主要取决于编译器。大部分编译器对无法`inline`的函数都会抛出一个警告信息

* 有时候虽然编译器有意愿`inlining`某个函数，但可能还是为该函数生成一个函数本体。例如，如果程序需要取某个`inline`函数的地址，编译器通常必须为此函数生成一个`outlined`函数本体。编译器通常不对“通过函数指针而进行的调用”实施`inlining`，这意味着`inline`函数的调用可能被`inlined`，也可能不被`inlined`，取决于该调用的实施方式：

	```c++
	inline void f() { .. }
	void (*pf)()=f;
	...
	f();
	pf();
	```

* 有时候编译器会生成构造函数和析构函数的`outline`副本，构造函数和析构函数不适合进行`inlining`，即使其函数内容为空

	* 构造函数和析构函数并非真的为空，派生类构造函数至少一定会陆续调用其成员变量和基类两者的构造函数，这些调用会影响编译器是否对此空白函数`inlining`

* `inline`函数无法随程序库的升级而升级
	* 如果`f`是程序库内的一个`inline`函数，客户将`f`函数本体编进其程序中，一旦程序库设计者决定改变`f`，所有用到`f`的客户端程序都必须重新编译
	* 如果`f`是`non-inline`函数，一旦它有任何修改，客户端只需重新连接就好，远比重新编译的负担少很多。如果程序库采取动态链接，升级版函数甚至可以不知不觉地被应用程序吸纳

### Item 31：Minimize compilation dependencies between files

* C++“接口从实现分离”的缺陷：class的定义式不止详细叙述了class接口，还包括十足的实现细节

	```c++
	class Person{
	public:
	    Person(const std::string& name, cosnt Date& birthday, const Address& addr);
	    std::string name() const;
	    std::string birthDate() const;
	    std::string address() const;
	    ...
	private:
	    std::string theName;
	    Date theBirthDate;
	    Address theAddress;
	};
	```

	上述代码无法通过编译，因为找不到`std::string`，`Date`和`Address`的定义 ，需要包含相关头文件。而当相关依赖头文件修改时，每一个包含该头文件的源文件均需要进行编译

* 优化方法：以“声明的依存性”替换“定义的依存性”

	* 如果使用`object reference`或`object pointer`可以完成任务，就不要使用`object`
		* 定义一个类型的reference或pointer只需要一个类型声明式
		* 定义某类型的objects需要用到该类型的定义式
	* 尽量以class声明式替换class定义式

	* 为声明式和定义式提供不同的头文件
		* 类似`<iosfwd>`，`<iosfwd>`含`iostream`各组件的声明式，其对应定义则分布在若干不同的头文件内，包括`<sstream>`、`<streambuf>`、`<fstream>`和`<iostream>`

	```c++
	#include <string>
	#include <memory>
	
	class PersonImpl;	// Person实现类的前置声明
	class Date;
	class Address;
	
	class Person{
	public:
	    Person(const std::string& name, const Date& birthday, const Address& addr);
	    std::string name() const;
	    std::string birthDate() const;
	    std::string address() const;
	    ...
	private:
	    std::tr1::shared_ptr<PersonImpl> pImpl;
	};
	```

* 使用pimpl idiom的classes通常称为Handles classes

	* 将它们所有函数转交给相应的实现类并由后者完成实际工作

	```c++
	#include "Person.h"
	#include "PersonImpl.h"
	
	Person::Person(const std::string& name, const Date& birthday, const Address& addr)
		: pImpl(new PersonImpl(name, birthday, addr))
	{}
	std::string Person::name() const{return pImpl->name();}
	```

* Interface class：抽象基类，用于描述derived classes的接口，通常不带成员变量也没有构造函数，只有一个`virtual`析构函数和一组`pure virtual`函数来叙述整个接口

	```c++
	class Person{
	public:
	    virtual ~Person();
	    virtual std::string name() const = 0;
	    virtual std::string birthDate() const = 0;
	    virtual std::string address() const = 0;
	    ...
	};
	```

	* `interface class`的客户必须有办法为这种class创建对象。通常调用一个特殊函数，此函数扮演“真正被具现化”的那个derived classes的构造函数角色，这种函数通常称为工厂函数（factory）或virtual构造函数。它们返回指针，指向动态分配所得对象，而该对象支持interface class接口。这类函数在interface class中常声明为`static`如

		```c++
		class Person{
		public:
		    ...
		    static std::tr1::shared_ptr<Person> create(cosnt std::string& name, const Date& birthday, const Address& addr);
		    ...
		};
		```

	* 客户使用如下：

		```c++
		std::string name;
		Date dateOfBirth;
		Address address;
		
		std::tr1::shared_ptr<Person> pp(Person::create(name, dateOfBirth, address));
		...
		```

		支持interface class接口的那个具象类必须被定义出来，且真正的构造函数必须被调用，如下：

		```c++
		class RealPerson: public Person{
		public:
		    RealPerson(const std::string& name, const Date& birthday, const Address& addr)
		        : theName(name), theBirthDate(birthday), theAddress(addr)
		        {}
		    virtual ~RealPerson(){}
		    std::string name() const;
		    std::string birthDate() const;
		    std::string address() const;
		private:
		    std::string theName;
		    Date theBirthDate;
		    Address theAddress;
		};
		
		std::tr1::shared_ptr<Person> Person::create(cosnt std::string& name, const Date& birthday, const Address& addr)
		{
		    return std::tr1::shared_ptr<Person>(new RealPerson(name, birthday, addr));
		}
		```

		上述代码示范了interface classes的一种最常见机制：从interface class继承接口规范，然后实现出接口所覆盖的函数

* Handles classes和interface classes解除了接口和实现之间的耦合关系，降低文件之间的编译依存性

* 代价分析：

	* 对于Handles classes，成员函数必须通过implementation pointer取得对象数据。这将为每次访问增加一层间接性。而每一个对象消耗的内存数量必须增加implementation pointer的大小。最后implementation pointer必须进行初始化（在Handles classes构造函数内），指向一个动态分配得到的implementation object，因此将蒙受因动态内存分配及其释放所带来的额外开销，以及遭遇`bad_alloc`异常（内存不足）的可能

	* 对于Interface classes，由于每个函数都是`virtual`，因此每次调用都应付出一个间接跳跃代价。此外interface class派生对象必须内含一个virtual table pointer（vtpr），这个指针可能增加存放对象所需的内存数量——实际取决于这个对象除了interface class之外是否有其他virtual函数来源
	* 无论Handles classes还是Interface classes，一旦脱离`inline`函数都无法有太大作为

