---
title: python读取文件内容的三种方法
date: 2022-10-14 17:23:59
tags: python
categories: 学习
---
#这里介绍利用Python读取文本文件内容的三种方法：`read()`、`readline()`和`readlines()`。

假设`sxl.txt`文件内容如下：

```
i like the movie
i ate an egg
read()方法
```

## `read（）`方法表示一次读取文件全部内容，该方法返回字符串。

```python
f = open("sxl.txt")
lines = f.read()
print lines
print(type(lines))
f.close()
```
输出结果：

```
i like the movie
i ate an egg
<class 'str'>
```

## `readline（）`方法

该方法每次读出一行内容，所以，读取时占用内存小，比较适合大文件，该方法返回一个字符串对象。

```python
f = open("sxl.txt")
line = f.readline()
while line:
    print (line)
    print(type(line))
    line = f.readline()
f.close()
```

输出结果：

```
i like the movie
<class 'str'>
i ate an egg
<class 'str'>
```

## readlines（）方法

readlines()方法读取整个文件所有行，保存在一个列表(list)变量中，每次读取一行，但读取大文件会比较占内存。

```python
f = open("sxl.txt")
lines = f.readlines()
for line in lines:
    print (line)
    print(type(line))
f.close()
```

输出结果：

```
i like the movie
<class 'str'>
i ate an egg
<class 'str'>
```

最后还有一种方式，与第三种方法类似。

f = open("sxl.txt")
print (type(f))
for line in f:
    print (line)
    print(type(line))
f.close()
输出结果：

<class '_io.TextIOWrapper'>
i like the movie
<class 'str'>
i ate an egg
<class 'str'>

# OR


0.准备
假设a.txt的内容如下所示：

Hello
Welcome
What is the fuck...
1. read([size])方法
read([size])方法从文件当前位置起读取size个字节，若无参数size，则表示读取至文件结束为止，它范围为字符串对象

f = open("a.txt")
lines = f.read()
print lines
print(type(lines))
f.close()
输出结果：

Hello
Welcome
What is the fuck...
<type 'str'> #字符串类型
2.readline()方法
从字面意思可以看出，该方法每次读出一行内容，所以，读取时占用内存小，比较适合大文件，该方法返回一个字符串对象。

f = open("a.txt")
line = f.readline()
print(type(line))
while line:
    print line,
    line = f.readline()
f.close()
输出结果：

<type 'str'>
Hello
Welcome
What is the fuck...
3.readlines()方法读取整个文件所有行，保存在一个列表(list)变量中，每行作为一个元素，但读取大文件会比较占内存。
f = open("a.txt")
lines = f.readlines()
print(type(lines))
for line in lines:
    print line，
f.close()
输出结果：
<type 'list'>
Hello
Welcome
What is the fuck...

4.linecache模块
当然，有特殊需求还可以用linecache模块，比如你要输出某个文件的第n行：

# 输出第2行
text = linecache.getline(‘a.txt’,2)
print text,
对于大文件效率还可以。
