---
title: linux中sh文件书写格式
date: 2022-10-19 12:30:04
tags: linux
categories: 系统
---

# linux下执行.sh文件的方法

> `.sh`文件就是文本文件，如果要执行，需要使用`chmod a+x xxx.sh`来给可执行权限。 
  
是bash脚本么

可以用`touch test.sh`创建`test.sh`文件`vi test.sh`编辑`test.sh`文件

加入内容

```sh
#！/bin/bash
mkdir test
```
  
保存退出。

`chmod a+x test.sh`给`test.sh`可执行权限

如`test.sh`文件在`/home/work`文件下

执行

> 方法一 本身目录下运行

进入`cd /home/workwen`文件下

执行`./test.sh`

命令会在当前目录下创建一个`“test”`目录。

> 方法二 绝对路劲运行

执行`/home/work/test.sh`

> 方法三 本身目录下运行

`sh test.sh`

<!-- 
C代码

1.man sh

man sh 来看看sh 的介绍～

linux.sh语法 
-->

## 介绍

1. 开头

程序必须以下面的行开始（必须放在文件的第一行）：

```sh
#!/bin/sh
```

符号`#!`用来告诉系统它后面的参数是用来执行该文件的程序。在这个例子中我们使用`/bin/sh`来执行程序。

当编写脚本完成时，如果要执行该脚本，还必须使其可执行。

要使编写脚本可执行：

编译`chmod +x filename`这样才能用`./filename`来运行

2. 注释

在进行`shell`编程时，以#开头的句子表示注释，直到这一行的结束。我们真诚地建议您在程序中使用注释。

如果您使用了注释，那么即使相当长的时间内没有使用该脚本，您也能在很短的时间内明白该脚本的作用及工作原理。

3. 变量

在其他编程语言中您必须使用变量。在shell编程中，所有的变量都由字符串组成，并且您不需要对变量进行声明。要赋值给一个变量，您可以这样写：

```sh
#!/bin/sh
 #对变量赋值：
 a=”hello world”
# 现在打印变量a的内容：
 echo “A is:”
 echo $a
```

有时候变量名很容易与其他文字混淆，比如：

```bat
num=2
echo “this is the $numnd”
```

这并不会打印出`this is the 2nd`，而仅仅打印`this is the`，因为`shell`会去搜索变量`numnd`的值，但是这个变量时没有值的。可以使用花括号来告诉`shell`我们要打印的是`num`变量：

```sh
num=2
echo “this is the ${num}nd”
```

这将打印： `this is the 2nd`

4. 环境变量

由`export`关键字处理过的变量叫做环境变量。我们不对环境变量进行讨论，因为通常情况下仅仅在登录脚本中使用环境变量。

5. Shell命令和流程控制

在shell脚本中可以使用三类命令：

1)Unix 命令:

虽然在shell脚本中可以使用任意的unix命令，但是还是由一些相对更常用的命令。这些命令通常是用来进行文件和文字操作的。

常用命令语法及功能

echo “some text”: 将文字内容打印在屏幕上

ls: 文件列表

wc –l file   wc -w file   wc -c file: 计算文件行数；计算文件中的单词数；计算文件中的字符数

cp sourcefile destfile: 文件拷贝

mv oldname newname : 重命名文件或移动文件

rm file: 删除文件

grep ‘pattern’ file: 在文件内搜索字符串比如：grep ’searchstring’ file.txt

cut -b colnum file: 指定欲显示的文件内容范围，并将它们输出到标准输出设备比如：输出每行第5个到第9个字符cut -b5-9 file.txt千万不要和cat命令混淆，

这是两个完全不同的命令

cat file.txt: 输出文件内容到标准输出设备（屏幕）上

file somefile: 得到文件类型

read var: 提示用户输入，并将输入赋值给变量

sort file.txt: 对file.txt文件中的行进行排序

uniq: 删除文本文件中出现的重复行，比如： sort file.txt | uniq

expr: 进行数学运算Example: add 2 and 3   为   expr 2 “+” 3

find: 搜索文件比如：根据文件名搜索find . -name filename -print

tee: 将数据输出到标准输出设备(屏幕) 和文件比如：somecommand | tee outfile

basename file: 返回不包含路径的文件名比如： basename /bin/tux将返回 tux

dirname file: 返回文件所在路径比如：dirname /bin/tux将返回 /bin

head file: 打印文本文件开头几行

tail file : 打印文本文件末尾几行

sed: Sed是一个基本的查找替换程序。可以从标准输入（比如命令管道）读入文本，并将结果输出到标准输出（屏幕）。该命令采用正则表达式（见参考）进行搜索。不要和shell中的通配符相混淆。比如：将linuxfocus替换为 LinuxFocus ：cat text.file | sed ’s/linuxfocus/LinuxFocus/’ >newtext.file

awk: awk 用来从文本文件中提取字段。缺省地，字段分割符是空格，可以使用-F指定其他分割符。

cat  file.txt | awk -F, ‘{print $1 “,” $3}’这里我们使用，作为字段分割符，同时打印第一个和第三个字段。如果该文件内容如下： Adam Bor, 34, IndiaKerryMiller, 22, USA命令输出结果为：Adam Bor, IndiaKerry Miller, USA

2) 概念: 管道, 重定向和 backtick

这些不是系统命令，但是他们真的很重要。

管道 (|) 将一个命令的输出作为另外一个命令的输入。

grep “hello” file.txt | wc -l

在file.txt中搜索包含有”hello”的行并计算其行数。

在这里grep命令的输出作为wc命令的输入。当然您可以使用多个命令。

重定向：将命令的结果输出到文件，而不是标准输出（屏幕）。

> 写入文件并覆盖旧文件

>> 追加到文件的尾部，保留旧文件内容。

反短斜线

使用反短斜线可以将一个命令的输出作为另外一个命令的一个命令行参数。

命令：

find . -mtime  -1  -type  f  -print

用来查找过去24小时（-mtime –2则表示过去48小时）内修改过的文件。如果您想将所有查找到的文件打一个包，则可以使用以下linux 脚本：

```sh
#!/bin/sh
# The ticks are backticks (`) not normal quotes (‘):
tar -zcvf  lastmod.tar.gz `find . -mtime -1 -type f -print`
```

3) 流程控制

1.if

“if” 表达式 如果条件为真则执行then后面的部分：

```sh
if ….; then
….
elif ….; then
….
else
….
fi
```

大多数情况下，可以使用测试命令来对条件进行测试。比如可以比较字符串、判断文件是否存在及是否可读等等…

通常用” [ ] “来表示条件测试。注意这里的空格很重要。要确保方括号的空格。

[ -f "somefile" ] ：判断是否是一个文件

[ -x "/bin/ls" ] ：判断/bin/ls是否存在并有可执行权限

[ -n "$var" ] ：判断$var变量是否有值

[ "$a" = "$b" ] ：判断$a和$b是否相等

执行man test可以查看所有测试表达式可以比较和判断的类型。

直接执行以下脚本：

```bat
#!/bin/sh
if [ "$SHELL" = "/bin/bash" ]; then
echo “your login shell is the bash (bourne again shell)”
else
echo “your login shell is not bash but $SHELL”
fi
```

变量$SHELL包含了登录shell的名称，我们和/bin/bash进行了比较。

快捷操作符

熟悉C语言的朋友可能会很喜欢下面的表达式：

[ -f "/etc/shadow" ] && echo “This computer uses shadow passwors”

这里 && 就是一个快捷操作符，如果左边的表达式为真则执行右边的语句。

您也可以认为是逻辑运算中的与操作。上例中表示如果/etc/shadow文件存在则打印” This computer uses shadow passwors”。同样或操作(||)在shell编程中也是可用的。这里有个例子：

```bat
#!/bin/sh
mailfolder=/var/spool/mail/james
[ -r "$mailfolder" ]‘ ‘{ echo “Can not read $mailfolder” ; exit 1; }
echo “$mailfolder has mail from:”
grep “^From ” $mailfolder
```

该脚本首先判断mailfolder是否可读。如果可读则打印该文件中的”From” 一行。如果不可读则或操作生效，打印错误信息后脚本退出。这里有个问题，那就是我们必须有两个命令：

◆打印错误信息

◆退出程序

我们使用花括号以匿名函数的形式将两个命令放到一起作为一个命令使用。一般函数将在下文提及。

不用与和或操作符，我们也可以用if表达式作任何事情，但是使用与或操作符会更便利很多。

<!-- 
https://blog.csdn.net/ljp812184246/article/details/52585650 
-->