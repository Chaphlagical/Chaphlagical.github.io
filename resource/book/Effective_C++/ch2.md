## 2. Constructors, Destructors, and Assignment Operators

### Item 5: Know what functions C++ silently writes and calls

* C++对类会提供默认的函数，所有这些函数都是`public`且`inline`的

	* 默认函数包括`default`构造函数，`copy`构造函数，`copy assignment`操作符，析构函数

* 下面两块代码等价：

	```c++
	class Empty{};
	```

	```c++
	class Empty{
	public:
	    Empty(){...}
	    Empty(const Empty& rhs){...}
	    
	    ~Empty(){...}
	    
	    Empty& operator=(const Empty& rhs){...}
	}
	```

* 编译器产生的析构函数是个`non-virtual`函数，除非这个class 的基类自身声明有`virtual`析构函数

* 编译器生成的复制构造函数和复制赋值操作符简单地复制了源对象每个非静态数据成员到目标对象

### Item 6: Explicitly disallow the use of compiler-generated functions you do not want

* C++的默认构造函数和析构函数是自动生成的，如不需要，必须手动进行禁用

* 可以将相关函数声明为`private`并且不去定义它

	```c++
	class HomeForSale{
	public:
	    ...
	private:
	    ...
	    HomeForSale(const HomeForSale&);
	    HomeForSale& operator=(const HomeForSale&);
	};
	```

* 也可以通过设计以下类进行继承以减少代码重复：

	```c++
	class Uncopyable{
	protected:
	    Uncopyable(){}
	    ~Uncopyable(){}
	    
	private:
	    Uncopyable(const Uncopyable&);
	    Uncopyable& operator=(const Uncopyable&);
	};
	```

	使用时，只需要

	```c++
	class HomeForScale:private Uncopyable{
	    ...
	};
	```

### Item 7: Declare destructors virtual in polymorphic base classes

* 对于多态类，可以定义一个基类及其派生类，利用指向基类的指针，重新指向派生类进行操作
* 但对指向派生类的基类指针进行内存释放时，指针将作为基类指针进行删除，如果基类存在一个非`virtual`析构函数，则只会删除所指派生类的基类部分，而对于派生类剩余部分将造成内存泄漏
* 解决方法：将基类的析构函数声明为`virtual`函数，删除派生类时将会把整个对象删除，包括派生类部分
* `virtual`函数的原理：
	* 要实现`virtual`函数，对象必须携带某些信息，主要用来在运行期决定哪个`virtual`函数该被调用
	* 该信息由虚表指针（vptr，virtual table pointer）指针指出
	* vptr指向一个由函数指针构成的数组，称为虚表(vtbl，virtual table)
	* 每一个带有`virtual`函数的class都有相应的`vtbl`
	* 当对象调用某一`virtual`函数，实际被调用的函数取决于该对象的vptr所指向的那个vtbl——编译器在其中寻找合适的函数指针
* 如果一个类不打算作为基类或为了具备多态性，则最好不要使用`virtual`函数
* 多态基函数应该声明一个`virtual`析构函数，如果class带有任何virtual函数，就应该拥有一个virtual析构函数
* 如果类中含有纯`virtual`函数，则该类将变成抽象函数，不能进行实例化
	* 如果希望声明一个没有纯`virtual`成员函数的抽象类，可以在类中声明一个纯`virtual`的析构函数
	* 纯`virtual`析构函数应提供定义
* 为基类提供`virtual`拟析构函数的规则仅适用于多态基类，并非所有基类都会用于多态
	* STL容器均不设计为基类
	* 像`Uncopyable`这类基类也不设计为多态

### Item 8: Prevent exceptions from leaving destructors

* C++的析构函数中发生异常是一件很麻烦的事

* 一般C++程序发生异常可能会出现两种情况：

	1. 程序提前终止
	2. 程序发生未知行为

	而析构函数发生异常时常出现第二种情况

* 解决方法：

	1. 手动终止程序

		```c++
		DBConn::~DBConn()
		{
		    try{db.close();}
		    catch (...){
		        //	Log here
		        std::abort();
		    }
		}
		```

		当程序无法正常运行时将进入异常处理函数，调用`abort`以结束程序

	2. 忽略异常

		```c++
		DBConn::~DBConn()
		{
		    try{db.close();}
		    catch (...){
		        //	Log here
		    }
		}
		```

		一般情况下不推荐做法，但在程序要求持续可靠运行时是个不错的选择
		
	3. 重新设计接口（推荐做法）
	
		```c++
		class DBConn{
		public:
		    ...
		    void close()
		    {
		        db.close();
		        closed=true;
		    }
		    ~DBConn()
		    {
		        if(!closed){
		            try{
		                db.close();
		            }
		            catch(...){
		                // logging
		                ...
		            }
		        }
		    }
		private:
		    DBConnection db;
		    bool closed;
		};
		```
	
		* 提供自身的`close`函数，赋予客户端一个机会得以手动处理异常
		* 同时`DBConn`也可追踪其管理的`DBConnection`是否关闭，并在答案为否的时候调用析构函数将其关闭

---

### Item 9: Never call virtual functions during construction or destruction

* 在构造函数和析构函数中不应该调用`virtual`函数，因为所调用的`virtual`函数可能不是你想调用的那个`virtual`函数，举例：

	```c++
	class Transaction{
	public:
	    Transaction();
	    virtual void logTransaction() const = 0;
	    ...
	};
	Transaction::Transaction()
	{
	    ...
	    logTransaction();
	}
	class BugTransaction:public Transaction{
	public:
	    virtual void logTransaction() const;
	    ...
	};
	class SellTransaction:public Transaction{
	public:
	    virtual void logTransaction() const;
	    ...
	};
	
	// 执行
	BuyTransaction b;
	```

	* 在调用`BuyTransaction`构造函数之前，基类`Transaction`构造函数会先被调用
	* `Transaction`构造函数调用了`virtual`函数，且该`virtual`函数此时为`Transaction`版本
	* 对象在派生类构造函数开始执行前不会成为一个派生类对象
		* 因为此时派生类成员变量未定值

* 一个潜藏的问题

	```c++
	class Transaction{
	public:
	    Transaction(){init();}
	    virtual void logTransaction() const = 0;
	    ...
	private:
	    void init()
	    {
	        ...
	        logTransaction();
	    }
	};
	```

	* 构造函数调用得函数中带有`virtual`函数
	* 若`virtual`函数为纯`virtual`函数时，将发生链接错误
	* 而若`virtual`函数有定义时，派生类的构造将得到错误的结果

* 假设有一个基类和多个派生类，基类的构造函数中调用了一个`virtual`成员函数，此时需要定义一个派生类对象
	* 若`virtual`函数为纯`virtual`函数，基类构造函数将调用一个基类下的纯`virtual`函数，发生错误
	* 若`virtual`函数为普通`virtual`函数，基类构造函数将调用一个基类下的`virtual`函数，而不是派生类中的多态函数，无法将派生类的信息传递到基类
	
* 解决问题的方法：
	* 使用`explicit`关键字修饰带参数的构造函数
	* 将原来的`virtual`成员函数定义为非`virtual`成员函数
	* 在派生类中，使用成员初始化列表对基类进行传参初始化，这样即实现了将信息从派生类传递到基类的构造函数中
	
	举例：
	
	```c++
	class Transaction{
	public:
	    explicit Transaction(const std::string& logInfo);
	    void logTransaction(const std::string& logInfo) const;
	    ...
	};
	Transaction::Transaction(const std::string& logInfo)
	{
	    ...
	    logTransaction(logInfo);
	}
	class BuyTransaction: public Transaction{
	public:
	    BuyTransaction(parameters)
	        :Transaction(createLogString(parameters))
	        {...}
	    ...
	private:
	    static std::string createLogString(parameters);
	};
	```
	
	* 令派生类将必要的构造信息向上传到基类构造函数

### Item 10: Have assignment operators return a reference to \*this

* C++支持链式赋值操作：

	```c++
	int x,y,z;
	x=y=z=15;
	```

	也等价于

	```c++
	x=(y=(z=15))
	```

* 因此在定义赋值运算符重载时，最好也返回`*this`

	```c++
	class Widget{
	public:
	    ...
	        
	    Widget& operator=(const Widget& rhs)
	    {
	        ...
	        return *this;
	    }
	    
	    Widget& operator+=(const Widget& rhs)
	    {
	        ...
	        return *this;
	    }
	    
	    Widget& operator*=(const Widget& rhs)
	    {
	        ...
	        return *this;
	    }
	    ...
	}
	```
* 这只是个协议规范，并无强制性

### Item 11: Handle assignment to self in operator=

* 将本身的值赋值给本身往往容易出现错误，例如：

  ```c++
  class Bitmap{...};
  class Widget{
      ...
  private:
      Bitmap* pb;
  };
  
  Widget& Widget::operator=(const Widget& rhs)
  {
      delete pb;
      pb=new Bitmap(*ths.pb);
      
      return *this;
  }
  ```

  这里`ths`可能就是其自己本身，而整个代码运行后将返回一个指向已删除对象的指针

* 传统的解决方法是进行测试

	```c++
	Widget& Widget::operator=(const Widget& rhs)
	{
	    if(this==&rhs)return *this;
	    
	    delete pb;
	    pb=new Bitmap(*rhs.pb);
	    
	    return *this;
	}
	```

	这种方法是有缺陷的，假设在新建`Bitmap`的过程中出现异常，得到的指针将是有害的，你将不能安全的删除它们，甚至是读取它们

* 一种安全的做法是保存下指针原来所指的值

	```c++
	Widget& Widget::operator=(const Widget& rhs)
	{
	    Bitmap *pOrig = pb;
	    pb = new Bitmap(*rhs.pb);
	    delete pOrig;
	    
	    return *this;
	}
	```

	需要复制，效率不够高

* 复制和交换（copy and swap）技术。确保实现既是异常安全又是复制安全

	```c++
	Widget& Widget::operator=(const Widget& rhs)
	{
	    Widget temp(rhs);
	    
	    swap(temp);	// 交换*this和*temp
	    return *this;
	}
	```

---

### Item 12: Copy all parts of an object

* 一般的复制函数包括：复制构造函数和复制赋值运算符

* 默认的复制函数将复制对象中所有的数据

* 自定义的复制函数必须要把所有数据都进行拷贝（包括基类数据）

	* 注意类继承时容易出现不完全拷贝的情况，复制函数应确保复制对象内所有成员变量和所有基类成分

	```c++
	class Data{...}
	
	class Customer{
	public:
	    ...
	   
	private:
	    std::string name;
	    Data lastTransaction;
	};
	
	class PriorityCustomer: public Customer{
	public:
	    ...
	    PriorityCustomer(const PriorityCustomer& rhs);
	    PriorityCustomer& operator=(const PriorityCustomer& rhs);   
	    ...
	
	private:
	    int priority;
	};
	
	PriorityCustomer::PriorityCustomer(const PriorityCustomer& rhs)
	    :Customer(rhs),priority(ths.priority)
	{
	    logCall("PriorityCustomer copy constructor"); 
	}
	
	PriorityCustomer& PriorityCustomer::operator=(const PriorityCustomer& rhs)
	{
	     logCall("PriorityCustomer copy assignment operator");
	    Customer::operator=(rhs);
	    priority=rhs.priority;
	    
	    return *this;
	}
	```
