---
title: linux设置开机启动（待完善）
date: 2022-10-19 12:29:54
tags: linux
categories: 系统
---
话不多说，本文介绍几种方法，希望能够对你的胃口。
文章目录
一、编辑/etc/rc.d/rc.local文件
二、crontab计划任务
三、使用systemd，自己写个服务就ok了
四、在/etc/profile.d/下写.sh文件
五、使用chkconfig管理，编辑/etc/init.d/下文件
一、编辑/etc/rc.d/rc.local文件
在linux各项服务启动完毕之后，会运行/etc/rc.d/rc.local这个文件，所以把我们需要运行的脚本放在这里面就行了。
（ps：/etc/rc.local和/etc/rc.d/rc.local是同一个文件，软链接而已）

# cat /mnt/Autorun_script.sh
date > /tmp/bootup.txt
hostname >> /tmp/bootup.txt
echo `whoami` >> /tmp/bootup.txt
1
2
3
4
将/mnt/Autorun_script.sh这个脚本放到/etc/rc.d/rc.local这个文件最后一行


最后为了保险起见，别忘了加一个权限

chmod  +x /mnt/Autorun_script.sh
chmod +x /etc/rc.d/rc.local
1
2
重启效果见下


二、crontab计划任务
可以自己设置时间，下面介绍另一个特殊的任务，叫@reboot，重启之后自动运行脚本。

效果见下


三、使用systemd，自己写个服务就ok了
上面介绍的两种方法，在任何的linux系统上都可以运行。第三种是适用systemd系统的，那么如何判定你的系统是不是systemd系统，运行ps命令

PID为1的进程是systemd就是，反之。
所以接下来，我们开始写systemd启动服务，并放在/etc/systemd/system/下。

写完之后我们更新一下systemd的配置文件,大功告成。

systemctl daemon-reload
systemctl enable Autorun_script.service
1
2
四、在/etc/profile.d/下写.sh文件
在/etc/profile.d/下写.sh文件，reboot即可
/etc/profile会遍历/etc/profile.d/*.sh


另外，几个脚本的区别：
（1） /etc/profile： 此文件为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行. 并从/etc/profile.d目录的配置文件中搜集shell的设置。

（2） /etc/bashrc: 为每一个运行bash shell的用户执行此文件.当bash shell被打开时,该文件被读取（即每次新开一个终端，都会执行bashrc）。

（3） ~/.bash_profile: 每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该文件仅仅执行一次。默认情况下,设置一些环境变量,执行用户的.bashrc文件。

（4） ~/.bashrc: 该文件包含专用于你的bash shell的bash信息,当登录时以及每次打开新的shell时,该文件被读取。你可以在这里设置你的个性化终端了，就像下面这样


（5） ~/.bash_logout: 当每次退出系统(退出bash shell)时,执行该文件. 另外,/etc/profile中设定的变量(全局)的可以作用于任何用户,而~/.bashrc等中设定的变量(局部)只能继承 /etc/profile中的变量,他们是”父子”关系。

（6） ~/.bash_profile: 是交互式、login 方式进入 bash 运行的。~/.bashrc 是交互式 non-login 方式进入 bash 运行的通常二者设置大致相同，所以通常前者会调用后者。

五、使用chkconfig管理，编辑/etc/init.d/下文件
详细操作方法请看我的另一篇博客[点我看方法](https://blog.csdn.net/qq_44839276/article/details/107624188)
————————————————
版权声明：本文为CSDN博主「Hejing_zhang」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_44839276/article/details/107622265