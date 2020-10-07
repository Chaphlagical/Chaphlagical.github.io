## 1. Accustoming Yourself to C++

### Item 1: View C++ as a federation of languages

* C++的多重范型性：支持过程形式、面向对象形式、函数形式、泛型形式、元编程形式

* 将C++视为次语言的集合：
	* C：区块blocks、语句statements、预处理器preprocessor，内置数据结构built-in data types、数组arrays、指针pointers等
	* Object-Oriented C++：classes（构造与析构函数）、封装encapsulation、继承inheritance、多态polymorphism、virtual函数（动态绑定）等
	* Template C++：模板元编程TMP
	* STL：template程序库，容器containers、迭代器iterators、算法algorithms、函数对象function objects

### Item 2: Prefer consts, enums, and inlines to \#define

 **`#define`的缺陷**

* `#define`不会被编译器看到，甚至在预处理期就被替换掉了，名称不会进入符号表，直接替换成目标，容易造成调试上的困难

	* 例如：

		```c++
		#define ASPECT_RATIO 1.653
		```

		当使用常量`ASPECT_RATIO`且获得一个编译错误信息时，该错误信息可能提到1.653而不是`ASPECT_RATIO`，追踪与调试将带来麻烦

* `#define`定义的宏可以实现类似函数的功能，且不会带来函数调用的开销，但是宏也存在很大的缺陷

	* 例如：

		```c++
		#define CALL_WITH_MAX(a,b) f((a)>(b)?(a):(b))
		```

		编写宏时应给每个变量加括号，但即使加了括号还是会有自增自减次数问题，如：

		```c++
		int a=5,b=0;
		CALL_WITH_MAX(++a,b);		// a被累加两次
		CALL_WITH_MAX(++a,b+10);	// a被累加一次
		```

**用`const`修饰常量**

* `const`修饰的常量名称能够被编译器看到，会进入符号表

* `const`修饰常量指针，通常定义在头文件中，对于常量字符串，最好如下定义：

	```c++
	const char* const authorName = "Scott Meyers";	// char*-base
	const std::string authorName = "Scott Meyers";	// string class
	```

* `const`修饰class专属常量，为了将常量的作用域限制在class内，需要让它成为class的一个成员，且声明为`static`以保证此常量至多只有一份实体，例如：

	```c++
	class GamePlayer{
	private:  
	    static const int NumTurns = 5;	// 声明并定义
	    int scores[NumTurns];
	    ...
	};
	
	class CostEstimate{
	private:
	    static const double FudgeFactor;	// 头文件内声明
		...
	};
	const double ConstEstimate::FudgeFactor = 1.35;	// 在实现文件中定义
	```

**用`enum`修饰常量**

* `enum`比`const`更接近于`#define`，`const`修饰的常量可取地址而`enum`修饰的不能（可用于保护常量），`enum`不会造成不必要的内存申请（避免他人对该常量取地址取指针）

* `enum`是模板元编程的基础技术

* 举例：

	```c++
	class GamePlayer{
	private:
	    enum{ NumTurns = 5 };
	    int scores[NumTurns];
	    ...
	};
	```

**用`inline`代替宏**

* 使用`inline`关键字定义内联函数，例如：

	```c++
	template<typename T>
	inline void callWithMax(const T& a, const T& b)
	{
	    f(a>b?a:b);
	}
	```

### Item 3: Use const whenever possible

**`const`修饰指针与常量的用法**

* 当`const`在星号左侧时，指针指向的为常值
* 当`const`在星号右侧时，指针本身为常值
* 当`const`星号两侧都有时，指针本身及其指向均为常值
* 当指针指向常值时，`const`在类型名前后意思相同

```c++
char greeting[] = "Hello";
char* p = greeting;				// non-const pointer, non-const data
const char* p = greeting;		// non-const pointer, const data
char* const p = greeting;		// const pointer, non-const data
const char* const p = greeting;	// const pointer, const data
void f1(const Widget *pw);
void f1(Widget const *pw);	// 两个意思相同
```

**STL迭代器的`const`**

* `const iterator`相当于`T* const`
* `const_iterator`相当于`const T*`

```c++
std::vector<int> vec;
...
const std::vector<int>::iterator iter = vec.begin();	// 相当于T* const
*iter = 10;	// 正确
++iter;		//错误
std::vector<int>::const_iterator cIter = vec.begin();	// 相当于const T*
*cIter = 10;// 错误
++cIter;	// 正确
```

**`const`修饰函数返回值**

* 降低客户错误而造成的意外，又不至于放弃安全性和高效性

```c++
class Rational{...}
const Rational operator*(const Rational& lhs, const Rational& rhs);
```

* 若不加`const`，则错误`(a*b)=c`（实际是想进行比较`(a*b)==c`）将难以被发现

**`const`修饰成员函数**

* 目的：

	* 使得class接口比较容易被理解
	* 使“操作const对象”成为可能

* 举例：

```c++
class TextBlock{
public:
...
    const char& operator[](std::size_t position) const
    { return text[position]; }	// 返回const对象
    char& operator[](std::size_t position)
    { return text[position]; }	// 返回non-const对象
private:
    std::string text;
};

// usage
TextBlock tb("Hello");
TextBlock ctb("Hello");

std::cout<<tb[0];	// 正确，读non-const
tb[0]='x';			// 正确，写non-const
std::cout<<ctb[0];	// 正确，读const
ctb[0]='x';			// 错误，写const
```

* Bitwise-constness & Logical-constness

	* Bitwise-constness：成员函数只有在不更改对象的任何成员变量（static除外）时才可说是const

	* Logical-constness：一个const成员函数可以修改它所处理对象内的某些bits，但只有在客户端侦测不出来的情况下才满足const
		* 使用`mutable`关键字，使得成员变量能够在const成员函数内被修改，例如：

		```c++
		class CTextBlock{
		public:
    ...
		    std::size_t length() const;
		private:
		    char* pText;
		    mutable std::size_t textLength;
		    mutable bool lengthIsValid;
		};
		std::size_t CTextBlock::length() const
		{
		    if(!lengthIsValid)
		    {
		        textLength = std::strlen(pText);
		        lengthIsValid = true;
		    }
		    return textLength;
		}
		```

**`const`和`non-const`成员函数避免重复**

* 使用类型转换
* 举例：

```c++
class TextBlock{
public:
    ...
    const char& operator[](std::size_t position) const
    {
        ...
        ...
        ...
        return text[position];
    }
    char& operator[](std::size_t position)
    {
        return const_cast<char&>(static_cast<const TextBlock&>(*this)[position]);
    }
    ...
};
```

* `static_cast`加`const`强制安全转换（防止出现递归调用）
* `const_cast`移除`const`

### Item 4: Make sure that objects are initialized before they're used

**内置类型的初始化**

* 对于无任何成员的内置类型，手工进行初始化
* 举例：

```c++
int x = 0;	// 手工初始化int
const char* text = "A C-style string";	// 对指针进行手工初始化

double d;
std::cin>>d;	//读取输入流以初始化
```

**成员对象的初始化**

* 内置类型以外的任何东西，初始化由构造函数constructors完成

* 成员对象的初始化：成员初值列表（member initialization list）

	* 举例：

	```c++
	class PhoneNumber{...};
	class ABEntry{
	public:
	    ABEntry(const std::string& name, const std::string& address, const std::list<PhoneNumber>& phones);
	private:
	    std::string theName;
	    std::string theAddress;
	    std::list<PhoneNumber> thePhones;
	    int numTimesConsulted;
	};
	/*
	ABEntry::ABEntry(const std::string& name, const std::string& address, const std::list<PhoneNumber>& phones)
	{
		theName = name;
		theAddress = address;
		thePhones = phones;
		numTimesConsulted = 0;
	}	// 赋值
	*/
	ABEntry::ABEntry(const std::string& name, const std::string& address, const std::list<PhoneNumber>& phones)
	    :theName(name),
		theAddress(address),
		thePhones(phones),
		numTimesConsulted(0)
	    { }	// 初始化
	```

	* 赋值 vs 初始化
		* 赋值：首先调用默认构造函数为成员变量赋初值，然后立刻再对它们赋新值
		* 使用成员初值列表避免赋值的问题，效率较高
	* 没有在成员初值列表中指定初值的成员变量：
		* 对于用户自定义类型的成员变量，将会自动调用其自身的默认构造函数
		* 对于内置类型的成员变量，则可能出现随机结果，带来问题

**初始化顺序问题**

* 一个源文件及其所有`#include`的文件称为一个编译单元translation unit

* 两种`static`对象：函数内的`static`对象称为local static对象，其他`static`对象称为non-local static对象

* 如果一个编译单元的non-local static对象的初始化用到另外一个不同的编译单元中的non-local static对象，则这个被用到的对象可能未被初始化

	* C++对定义不同编译单元中的non-local static对象的初始化顺序没有明确定义

* 解决方法：将每个non-local static对象移动到各自的函数，这些函数内把对象声明为static，函数的返回包含它们包含的对象的引用。客户端调用函数而不是直接使用对象，这样一来将non-local static对象转化为local static对象（实际上就是设计模式中的单例模式）

  * 原理：C++保证函数内的local-static对象会在"该函数被调用期间"以及"首次遇到该对象的定义式"时被初始化

  ```c++
  class FileSystem{...};
  
  FileSystem& tfs()
  {
      static FileSystem fs;
      return fs;
  }
  
  class Directory{...};
  
  Directory::Directory(params)
  {
      ...
      std::size_t disks = tfs().numDisks();
      ...
  }
  
  Directory& tempDir()
  {
      static Directory td;
      return td;
  }
  ```

* 这种方法在多线程系统内具有不确定性，解决方法：可以在程序的单线程启动部分期间手动调用所有返回引用的函数，消除与初始化相关的竞争形势

**小结**

初始化三部曲:

1. 手动初始化内置型non-member对象
2. 使用成员初值列表member initialization lists处理成员对象初始化
3. 针对初始化次序不确定性加强设计