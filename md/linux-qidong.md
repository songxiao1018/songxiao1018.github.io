---
title: linux系统开关机基本命令
date: 2022-10-19 12:53:09
tags: linux
categories: 系统
---
Linux中的重启命令： 1、“shutdown -r now”命令，停止系统服务后重启；2、“init 1”重启命令；3、“reboot”命令，立即重启；4、“poweroff”重启命令；5、“halt”重启命令。



程序员必备接口测试调试工具：
【相关文章推荐：linux教程】

Linux是一套免费使用和自由传播的类Unix操作系统，是一个基于POSIX和UNIX的多用户、多任务、支持多线程和多CPU的操作系统。它能运行主要的UNIX工具软件、应用程序和网络协议。它支持32位和64位硬件。Linux继承了Unix以网络为核心的设计思想，是一个性能稳定的多用户网络操作系统。

Linux 有五个重启命令

1、shutdown

shutdown是最常用也是最安全的关机和重启命令，它会在关机之前调用fsck检查磁盘，其中-h和-r是最常用的参数：





示例：











2、poweroff

poweroff表示立即关机，效果等同于shutdown -h now，在多用户模式下(Run Level 3）不建议使用。

3、init

























init是所有进程的祖先﹐它的进程号始终为1﹐所以发送TERM信号给init会终止所有的 用户进程﹑守护进程等。shutdown 就是使用这种机制。init定义了8个运行级别(runlevel)， init 0为关机﹐init 1为重启。

4、reboot

reboot表示立即重启，效果等同于shutdown -r now

5、halt

不理会目前系统状况下，进行硬件关机，一般不建议使用。

本篇文章就是关于Linux 重启命令的介绍，希望对需要的朋友有所帮助！

以上就是Linux 重启命令是什么？的详细内容，更多请关注php中文网其它相关文章！