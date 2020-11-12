# Chapter 1: Function Templates

## 1.1 A First Look at Function Templates

### 1.1.1 Defining the Templates

```C++
// max1.hpp
template<typename T>
T max(T a, T b)
{
    return b<a?a:b;
}
```

也可以使用关键词 `typename`:

```c++
template<class T>
T max(T a, T b)
{
    return b<a?a:b;
}
```

### 1.1.2. Using the Templates

```c++
#include "max1.hpp"
#include <iostream>
#include <string>

int main()
{
    int i = 42;
    std::cout << "max(7,i): " << ::max(7,i) << '\n';
    
    double f1 = 3.4;
    double f2 = -6.7;
    std::cout << "max(f1,f2)： " << ::max(f1,f2) << '\n';
    
    std::string s1="mathematics";
    std::string s2="math";
    std::cout<<"max(s1,s2): ">> ::max(s1, s2)<<"\n";
}
```

* 这里`::max()`是防止与标准库`std::max`冲突

### 1.1.3. Two-Phase Translation

1. definition time
   * 检查语法错误
   * 检查未知变量名错误（不依赖模板参数）
   * 静态断言（不依赖模板参数）
2. instantiation time
   * 再次确认模板代码有效（代入模板参数）

## 1.2. Template Argument Deduction

**Type Conversions During Type Deduction**

* 当声明为按引用传参时，必须要求模板参数一模一样，而无法进行任何的转换（[示例](https://cppinsights.io/lnk?code=Lyp0ZW1wbGF0ZTx0eXBlbmFtZSBUPgpUIG1heChUJiBhLCBUJmIpCnsKCXJldHVybiBhPmI/YTpiOwp9Ki8JLy8gdHJ5IGl0Cgp0ZW1wbGF0ZTx0eXBlbmFtZSBUPgpUIG1heChUIGEsIFQgYikKewoJcmV0dXJuIGE+Yj9hOmI7Cn0KCmludCBtYWluKCkKewoJaW50IGE9MTsKICAJaW50IGNvbnN0IGI9MjsKICAJaW50IGNvbnN0JiBjPTM7CiAgCW1heChhLGIpOwoJbWF4KGEsYyk7CiAgCglyZXR1cm4gMDsKfQ==&insightsOptions=cpp17&std=cpp17&rev=1.0)）
* 当声明为按值传参时，能够进行轻微的退化转化，而对多个参数其退化类型必须一致，如：
  * 忽略`const`和`volatile`
  * references转为referenced类型
  * raw arrays转为相应的指针类型

**Type Deduction for Default Arguments**

需要声明一个默认的模板参数，如：

```C++
template<typename T=std::string>
void f(T="");
```

## 1.3 Multiple Template Parameters

使用不同参数模板

```c++
template<typename T1, typename T2>
T1 max(T1 a, T2 b)
{
    return b<a?a:b;
}
```

> 返回类型只能有`T1`，解决方法如下：

### 1.3.1 Template Parameters for Return Types

增加一个新的模板参数类型：

```c++
template<typename T1, typename T2, typename RT>
RT max(T1 a, T2 b);
```

使用时可以显式调用：

```c++
::max<int, double, double>(4,7.2);
```

也可以调整模板参数类型的位置：

```c++
template<typename RT, typename T1, typename T2>
RT max(T1 a, T2 b);
```

然后仅指定返回类型：

```c++
::max<double>(4,7.2);
```

### 1.3.2 Deducing the Return Type

使用`decltype`：

```c++
template<typename T1, typename T2>
auto max(T1 a, T2 b)->decltype(b<a?a:b)
{
    return b<a?a:b;
}
```

可以直接用`true?a:b`代替`b<a?a:b`

```c++
template<typename T1, typename T2>
auto max(T1 a, T2 b)->decltype(true?a:b)
{
    return b<a?a:b;
}
```

有时候，`T`可能为引用，返回值需要为`T`的退化，可以使用`<type_traits>`库中的`std::decay_t<>`/`std::decay<>::type`

```c++
#include <type_traits>
template<typename T1, typename T2>
auto max(T1 a, T2 b)->typename std::decay_t<decltype(b<a?a:b)>
{
    return b<a?a:b;
}
```

* `std::decay_t`的作用是对变量进行退化类型处理，去掉引用、`const`等修饰

### 1.3.3 Return Type as Common Type

使用`<type_traits>`库中的`std::common_type_t<>`/`std::common_type<>::type`类型作为返回值类型：

```c++
#include <type_traits>
template<typename T1, typename T2>
std::common_type_t<T1,T2> max(T1 a, T2 b)
{
    return b<a?a:b;
}
```

## 1.4. Default Template Arguments



