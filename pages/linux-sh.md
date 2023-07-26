---
title: linux中sh文件使用方法
date: 2022-10-19 19:32:29
tags: linux
categories: 系统
---
linux sh命令简述
1. 可能需要的执行方式
linux下执行.sh文件的方法
2. 开头：#!/bin/sh
3. 变量
4. Shell命令和流程控制
Unix命令
概念：管道，重定向和backtick（反斜线）
流程控制
1. 可能需要的执行方式
linux下执行.sh文件的方法
.sh文件就是文本文件，如果要执行，需要使用chmod a+x xxx.sh来给可执行权限。

2. 开头：#!/bin/sh
shell程序必须以“#!/bin/sh”开始。shell中#一般表示注释的意思，所以很多时候认为"#!"也是注释，但实际上并不是。

"#!/bin/sh"是对shell的声明，说明你所用的是哪种类型的shell及其路径所在。

#!/bin/是指此脚本使用.bin/sh来执行。

#!是特殊的表示符，其后面跟的是解释此脚本的shell的路径，如果没有声明，则脚本将在默认的shell中执行，默认shell是由用户所在的系统定义为执行shell脚本，如果脚本被编写为在Kornshell ksh中运行，而默认运行shell脚本的为C shell csh,则脚本在执行过程中很可能失败。所以建议大家就把"#!/bin/sh"当成C 语言的main函数一样，写shell必须有，以使shell程序更严密。

3. 变量
在其他编程语言中必须使用变量。在shell编程中，所有变量都由字符串组成，并且不需要对变量进行声明。要赋值给一个变量，可以这样写：

#!/bin/sh
 #对变量赋值：
 a=”hello world”
# 现在打印变量a的内容：
 echo “A is:”
 echo $a
1
2
3
4
5
6
有时候变量名很容易与其他文字混淆，比如：

 num=2
 echo “this is the $numnd”
1
2
这并不会打印出”this is the 2nd"，而仅仅打印"this is the "，因为shell会去搜索变量numnd的值，但是这个变量是没有值的。因此，可以使用花括号来告诉shell我们要打印的是num变量：

 num=2
 echo “this is the ${num}nd”
1
2
这样才会打印”this is the 2nd"

4. Shell命令和流程控制
在shell脚本中可以使用以下命令：

Unix命令
虽然在shell脚本中可以使用任意的unix命令，但还是有一些相对更常用的命令。这些命令通常是用来进行文件和文字操作的。
如：

 echo "some text" #将文字内容打印在屏幕上
 ls #文件列表
 cp sourcefile destfile #文件拷贝
 mv oldname newname #重命名文件或移动文件
 rm file #删除文件
 grep 'pattern' file #在文件内搜索字符串，如：grep 'searchstring' file.txt
 cat file.txt #输出文件内容到标准输出设备（屏幕）上
 read var #显示用户输入，并将输入赋值给变量
1
2
3
4
5
6
7
8
概念：管道，重定向和backtick（反斜线）
管道 | 将一个命令的输出作为另外一个命令的输入。
grep "hello" file.txt | wc -l
1
上述代码表示为：在 file.txt 中搜索包含有 “hello” 的行并计算其行数。在这里grep命令的输出作为wc命令的输入。

需要注意的是，管道后的命令是子命令，并不会出现在接下来的命令中（有点像C++在{}内和{}外赋值的区别），如以下命令：

#!/bin/sh
echo 1 2 3 | { read a b c ; echo $a $b $c ; } # 打印结果为： 1 2 3
echo $a $b $c # 打印结果为空
1
2
3
重定向：将命令的结果输出到文件，而不是标准输出（屏幕）。
>写入文件并覆盖旧文件
>>追加到文件的尾部，保留旧文件内容。

反短横线 “`”：使用反短横线可以将一个命令的输出作为另一个命令的一个命令行参数。

 find . -mtime  -1  -type  f  -print
1
上述语句用来查找过去24小时（-mtime -2则表示过去48小时）内修改过的文件。如果想将所有查找到的文件打一个包，则可以使用一下linux脚本：

 #!/bin/sh
 # The ticks are backticks (`) not normal quotes (‘):
 tar -zcvf  lastmod.tar.gz `find . -mtime -1 -type f -print`
1
2
3
流程控制
if
if 表达式，如果条件为真则执行 then 后面的部分：

 if ….; then
 ….
 elif ….; then
 ….
 else
 ….
 fi #注意是以fi结尾
1
2
3
4
5
6
7
大多数情况下，可以使用测试命令来对条件进行测试。比如可以比较字符串、判断文件时都存在以及是否可读等等…

while
while 循环的语法结构为：

# expression 1
# while循环：当expresssion成立的时候，执行cmd
while (expresssion)
do
  cmd
done

# expression 2，可以直接使用true
while true（或 ：）
do 
	cmd
done  
1
2
3
4
5
6
7
8
9
10
11
12
该命令配合可以配合管道使用，如：

# 寻找 ${path} 路径下唯一首字母为‘E’的子目录，并 cd 到该目录
find ${path}/E* -type d | while read corresp_path
do
	cd ${corresp_path}
done
1
2
3
4
5
测试条件
通常使用“[ ]”来表示测试条件。注意这里的空格很重要，要确保方括号里的空格。

 [ -f "somefile" ] #判断文件是否存在
 [ -d "testResults/" ] #判断目录testResults/是否存在
 [ -x "/bin/ls" ] #判断/bin/ls文件是否存在并有可执行权限
 [ -n "$var" ] #判断$var变量是否有值
 [ "$a" = "$b" ] #判断$a和$b是否相等
1
2
3
4
5
快捷操作符
熟悉C语言可能会喜欢一下表达式：

  [ -f "/etc/shadow" ] && echo “This computer uses shadow passwors”
1
这里“&&”就是一个快捷操作符，如果左边的表达式为真则执行右边的语句。当然也可以将上述表达式认为是逻辑运算中的与操作。

同样或操作“||”在shell编程中也是可用的：

 #!/bin/sh
 mailfolder=/var/spool/mail/james
 [ -r "$mailfolder" ]‘ ‘{ echo “Can not read $mailfolder” ; exit 1; } #感觉这里的‘’应该是||
 echo “$mailfolder has mail from:”
 grep “^From ” $mailfolder
1
2
3
4
5
该脚本首先判断mailfolder是否可读。如果可读则打印该文件中的”From” 一行。如果不可读则或操作生效，打印错误信息后脚本退出。这里有个问题，那就是我们必须有两个命令：
◆打印错误信息
◆退出程序
我们使用花括号以匿名函数的形式将两个命令放到一起作为一个命令使用。一般函数将在下文提及。
不用‘与’和‘或’操作符，我们也可以用if表达式作任何事情，但是使用与或操作符会更便利很多。
————————————————
版权声明：本文为CSDN博主「泠山」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_28087491/article/details/107107342


---

https://www.php.cn/linux-421139.html

linux怎么执行sh文件
原创2019-05-29 16:56:5640961


本文介绍Linux下面用命令怎么执行.sh文件的方法，有两种方法：

一、直接./加上文件名.sh，如运行hello.sh为./hello.sh【hello.sh必须有x权限】

二、直接sh 加上文件名.sh，如运行hello.sh为sh hello.sh【hello.sh可以没有x权限】

方法一：当前目录执行.sh文件

【步骤一】cd到.sh文件所在目录

比如以hello.sh文件为例，如下图

b025c277daad47225f2a582b20c475c.png

【步骤二】给.sh文件添加x执行权限

比如以hello.sh文件为例，chmod u+x hello.sh，如下图

f871b7b1652765e6991f3d7fc4e8e92.png

【步骤三】./执行.sh文件

比如以hello.sh文件为例，./hello.sh 即可执行hello.sh文件，如下图

dab3467991cdb86c70255f48c1ca03c.png

【步骤四】sh 执行.sh文件

以hello.sh文件为例，sh hello.sh即可执行hello.sh文件，如下图

2ec0b33ee81cc50a16f47be2ae400c3.png

方法二：绝对路径执行.sh文件

下面三种方法都可以，如下图




./home/test/shell/hello.sh

/home/test/shell/hello.sh

sh /home/test/shell/hello.sh

60c14a51c0b1d39dfbfa312bdf8e9ab.png

注意事项：用“./”加文件名.sh执行时，必须给.sh文件加x执行权限。

以上就是linux怎么执行sh文件的详细内容，更多请关注php中文网其它相关文章！




