# Code Style Guide

!!! info
	Our C++ coding style is based off of [Google's C++ Style Guide](https://google.github.io/styleguide/cppguide.html). We use [clang-format](https://clang.llvm.org/docs/ClangFormat.html) to enforce most of the nit-picky parts of the style, such as brackets and alignment, so this document highlights the important rules to follow that clang-format cannot enforce.


## 变量

*  **Classes, structures, namespaces, unions, enumerates, "typename"-type template parameters, and typedefs** names uses `CamelCase` with a capital letter.

  ```cpp
  // Incorrect
  class eventHandler;

  // Incorrect
  class event_handler;

  // Correct
  class EventHandler;
  ```

*  **Constant variables** uses `ALL_CAPS_WITH_UNDERSCORES`. Constant variables include _static const_, _const class members_, _const_ global variables, and _const_ enumerations.

* **All variable** names are `lowercase_with_underscores`
  
  ```cpp
  // Incorrect
  float calculatedDistnace;
  
  // Correct
  float calculated_distance;
  ```
  
* **Function and method** names are `camelCase` with leader lowercase letter.
  
  ```cpp
  // Incorrect
  float get_distance();
  
  // Incorrect
  float GetDistance();
  
  // Correct
  float getDistance();
  ```
  
* Avoid "obvious" or "magic" numbers unless it's part of a mathematical or physics formula (ex `A=0.5(b*h)`).
  ```cpp
  // Incorrect
  float distance = catch_distance * 2.15;
  
  // Correct
  const float CATCH_DISTANCE_SCALE_FACTOR = 2.15;
  float distance = catch_distance * CATCH_DISTANCE_SCALE_FACTOR;
  ```
  
* Avoid initializing multiple variables on the same line.
  ```cpp
  // Incorrect
  int x, y, z = 0;
  
  // Correct and equivalent to the above
  int x;
  int y;
  int z = 0;
  
  // However, the author may have intended the following
  // or a code reader may have assumed the following
  int x = 0;
  int y = 0;
  int z = 0;
  ```


## 注释

Make sure to comment both the interface for a function or class, as well as the logic in the implementation. In general, try to make as many in-code documentations whenever possible.

As much code documentation as possible should live with the code itself \(in the form of comments\). This makes it easier for people working on the code to find the information, and because the code and comments are version-controlled together if we ever go back to an older version of the code, we will have the corresponding older documentation as well.

*Code comments are very important. Be sure to comment your code well enough so that another member of the team would be able to quickly get an understanding of what your code is doing, **and why**. Try not to make your comments unnecessarily verbose, but include as much detail you feel is necessary adequately explain the code. We realize that sounds contradictory, but use your best judgement as to what you think is clear and readable.*

If you think some ASCII art will help explain something better, go for it! [asciiflow](http://asciiflow.com/) is a good online tool for creating this.

* Comments regarding the interface of a class and its methods must be in the header file.
* In-code documentation comments and function comments follow the [javadoc style](https://www.tutorialspoint.com/java/java_documentation.htm).
  ```cpp
  // Incorrect
  // This function returns the power
  float power(float a, float b);
  
  // Correct
  /**
   * This function returns the power
   * @param a the base
   * @param b the exponent
   * @return a^b
   */
  float power(float a, float b);
  ```

## Get和Set函数
* in general, getter and setter methods on classes should be written like `getName()`, `setName(string name)`, with the following exceptions
  * getters with the return type `bool` may be prefixed with `is` instead of `get`, ie. `bool isActive()`
  * getters that are used _incredibly_ frequently and are _incredibly_ obvious may not require the `get` prefix. For example `Point::x()` and `Point::y()` 
  * getters that return specific units should be written as `toUnit()`. For example `Angle::toDegrees()`

## git commit message

**最关键的几点**

- 不同的事情尽量不要混在一次commit里面
- 讲清楚改了什么
- 不要commit一些与改动无关,自动改变的,如owl.ini

包括三个字段：`type`（必需）、`scope`（可选）和`subject`（必需）。

**（1）type**

`type`用于说明 commit 的类别，只允许使用下面7个标识。

> - feat：新功能（feature）
> - fix：修补bug
> - docs：文档（documentation）
> - style： 格式（不影响代码运行的变动）
> - refactor：重构（即不是新增功能，也不是修改bug的代码变动）
> - test：增加测试
> - chore：构建过程或辅助工具的变动

如果`type`为`feat`和`fix`，则该 commit 将肯定出现在 Change log 之中。其他情况（`docs`、`chore`、`style`、`refactor`、`test`）由你决定，要不要放入 Change log，建议是不要。

**（2）scope**

`scope`用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。

**（3）subject**

`subject`是 commit 目的的简短描述，不超过50个字符。

> - 以动词开头，使用第一人称现在时，比如`change`，而不是`changed`或`changes`
> - 第一个字母小写
> - 结尾不加句号（`.`）

详情见[git message编写指南]([Commit message 和 Change log 编写指南 - 阮一峰的网络日志](https://www.ruanyifeng.com/blog/2016/01/commit_message_change_log.html))

## 杂项

* All source files should have an empty line at the end of the file to avoid issues with GitHub.

* Avoid using C-style casts like `(int) x`. Use C++ casts such as static cast:
  ```cpp
  static_cast<int>(x);
  ```
  
* Simple data types \(`char`, `short`, `int`, `long`, `float`, `double`, `pointers`\) are generally pass by value.
  ```cpp
  void foo(double x);
  ```
  
* Non-simple data types are generally passed by _const_ references whenever possible. Try avoid setting values by reference, since this makes it harder to follow the flow of control and data in the program.
  ```cpp
  // Not ideal
  // Pass by reference to set data
  void getVisionPacket(Packet& packet);
  
  // Preferred
  // Pass by const reference
  Point predictBallPosition(const Ball& ball);
  ```


* All constructors should be marked with the `explicit` keyword. In the case of a one-argument constructor, this prevents it from being used as an implicit type conversion; in the case of other constructors, it acts as a safeguard in case arguments are later added or removed.
  ```cpp
  explicit AI(const World& world);
  ```
* Use C++ smart pointers and avoid raw pointers. (See also: [what are smart pointers and why they are good](https://stackoverflow.com/questions/106508/what-is-a-smart-pointer-and-when-should-i-use-one))
* Use C++11 keyword `using` to make _type alias_ instead of `typedef` as they're equivalent except the former is compatible with templates.
  ```cpp
  // Incorrect
  typedef std::vector<std::pair<int, int>> PointsArray;
  
  // Correct
  using PointsArray = std::vector<std::pair<int, int>>;
  ```
* Avoid initializing multiple variables on the same line.
  ```cpp
  // Incorrect
  int x, y, z = 0;
  
  // Correct
  int x;
  int y;
  int z = 0;
  
  // However, the author may have intended the following
  // or a code reader may have assumed the following
  int x = 0;
  int y = 0;
  int z = 0;
  ```
* Avoid ternary operators. Clarity is more important than line count.
  ```cpp
  // Incorrect
  c = ((a == 0) || ((a + b) < 10)) ? a : a + b;
  
  // Correct
  if ((a == 0) || ((a + b) < 10))
  {
    c = a;
  }
  else
  {
    c = a + b;
  }
  ```
* Always use curly braces around code blocks, even if the braces surround a single statement.
  ```cpp
  // Incorrect
  while (i < 10)
    i++;
    c[i] = i + 1;
  
  // Correct
  while (i < 10)
  {
    i++;
  }
  c[i] = i + 1;
  ```
