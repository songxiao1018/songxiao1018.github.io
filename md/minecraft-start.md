---
title: 我的世界linux和windows启动脚本
date: 2022-10-18 19:30:30
tags: 
 - linux
 - windows
 - mc
categories: Minecraft
---

# MC服务器启动脚本写法

1. Linux系统的.sh启动脚本

> Linux单次启动
> Linux循环十次启动
> Linux无限循环启动

1. Windows系统的.bat启动脚本

> Windows单次启动
> Windows循环十次启动
> Windows无限循环启动

## Minecraft服务器的启动脚本写法记录

首先，每个服务端都会有一个用于启动服务器的`jar`文件，这个根据具体情况具体修改，此处以`forge`直接启动服务器为例，使用文件`forge-1.12.2-14.23.5.2854.jar`启动服务器。

将服务端最低内存设置为1024M，最大内存设置为4096M，同时不需要图形界面，配置参数nogui。
核心的启动命令即为：

```java
java -server -XX:+UseG1GC  -Xmx4096M -Xms1024M -jar forge-1.12.2-14.23.5.2854.jar nogui
```

再随便瞎加一些优化参数（不一定是正优化，根据具体情况调整）

```java
java -server -XX:+UseG1GC  -Xms1024M -Xmx4096M -jar forge-1.12.2-14.23.5.2854.jar nogui -noverify -XX:+AggressiveOpts -XX:+UseCompressedOops
```

在完成了核心启动语句后，就要根据具体操作系统编写启动脚本了。

1. Linux系统的`.sh`启动脚本

新建任何一个后缀名为`.sh`的文件，使用`chmod +x`添加运行权限。

运行时使用`./文件名.sh`来运行文件。

1.1 Linux单次启动

```sh
#!/bin/sh

java -server -XX:+UseG1GC  -Xms1024M -Xmx4096M -jar forge-1.12.2-14.23.5.2854.jar nogui -noverify -XX:+AggressiveOpts -XX:+UseCompressedOops
```

1.2 Linux循环十次启动

服务器崩溃后会自动重新启动，一共启动十次，用于应对那些不是启动秒崩无限循环的小崩溃bug。

```sh
#!/bin/sh

for ((i=0; i<10; i ++))
do
    java -server -XX:+UseG1GC  -Xms1024M -Xmx4096M -jar forge-1.12.2-14.23.5.2854.jar nogui -noverify -XX:+AggressiveOpts -XX:+UseCompressedOops
done
```

1.3 Linux无限循环启动

崩溃后无限循环启动，只能通过强制终止`screen`或重启计算机停止。

```sh
#!/bin/sh

while ((1))
do
    java -server -XX:+UseG1GC  -Xms1024M -Xmx4096M -jar forge-1.12.2-14.23.5.2854.jar nogui -noverify -XX:+AggressiveOpts -XX:+UseCompressedOops
done
```

2. `Windows`系统的`.bat`启动脚本

新建任何一个后缀名为`.bat`的文件，运行时直接双击来运行文件。

> 注：`windows`系统的`cmd`如果要使用中文，需要用`GB2312`编码来编写`.bat`文件，否则中文会出现乱码问题。

2.1 `Windows`单次启动

单次启动的`.bat`脚本写法：

```bat
@ECHO OFF
title Minecraft Server
java -server -XX:+UseG1GC  -Xms1024M -Xmx4096M -jar forge-1.12.2-14.23.5.2854.jar nogui -noverify -XX:+AggressiveOpts -XX:+UseCompressedOops
pause
EXIT
```

2.2 `Windows`循环十次启动

服务器崩溃后会自动重新启动，一共启动十次，用于应对那些不是启动秒崩无限循环的小崩溃bug。

```bat
@ECHO OFF
title Minecraft Server
set n=0
:start_server
java -server -XX:+UseG1GC  -Xms1024M -Xmx4096M -jar forge-1.12.2-14.23.5.2854.jar nogui -noverify -XX:+AggressiveOpts -XX:+UseCompressedOops
set /a n+=1
if %n%==10 exit
goto start_server
```

2.3 `Windows`无限循环启动
崩溃后无限循环启动，可以通过关闭cmd窗口停止。

```bat
@ECHO OFF
title Minecraft Server
:start_server
java -server -XX:+UseG1GC  -Xms1024M -Xmx4096M -jar forge-1.12.2-14.23.5.2854.jar nogui -noverify -XX:+AggressiveOpts -XX:+UseCompressedOops
goto start_server
```

[](https://blog.csdn.net/starvapour/article/details/113415562)
[](https://www.cnblogs.com/anliven/articles/6847762.html)
