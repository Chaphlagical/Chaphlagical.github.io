# Chapter 1: Function Templates

## 1. Defining and Using Template

### 1.1. Defining the Templates

```C++
// max1.hpp
template<typename T>
T max(T a, T b)
{
    return b<a?a:b;
}
```

you can also use keyword `typename`:

```c++
template<class T>
T max(T a, T b)
{
    return b<a?a:b;
}
```

### 1.2. Using the Templates

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
    
    std::string
}
```

