---
title: linux-zip-tar
date: 2022-12-31 11:28:00
categories:
tags:
---
https://www.php.cn/linux-441774.html

Linux压缩命令（总结）
转载2020-01-23 13:35:2640866


Linux压缩命令

Linux常见的压缩格式有.zip、.gz、.bz2、.tar、.tar.gz、.tar.bz2；常用的压缩命令有zip、tar。这里列举了各压缩命令的使用示例。更多的用法请使用命令 --help查阅。

推荐：《Linux教程》

zip

格式：



zip [options] 目标压缩包名称 待压缩源文件

unzip [-Z] [options] 待压缩源文件 [list] [-x xlist] [-d exdir]

常用命令：









# 压缩文件

zip myfile.zip myfile

# 压缩文件夹（包含子目录）

zip -r mydir.zip mydir

# 压缩当前目录所有文件

zip mydir.zip *

# 解压文件

unzip mydir.zip

zip更多参数：















-v 显示操作详细信息

-d 从压缩包里删除文件

-m 将文件剪切到压缩包里，源文件将被删除

-r 递归压缩

-x 排除文件

-c 加一行备注

-z 加备注

-T 测试压缩包完整性

-e 加密

-q 安静模式

-1, --fast 更快的压缩速度

-9, --best 更好的压缩率

--help 查看帮助

-h2 查看更多帮助

unzip更多参数：










-v 显示操作详细信息

-l 查看压缩包内容

-d 解压到指定文件夹

-x 排除压缩包内文件

-t 测试压缩包文件内容

-z 查看备注

-o 覆盖文件无需提示

-q 安静模式

--help 查看帮助

示例：



$ ls

t.md  t.php t.php.zip
























































# 创建压缩包

$ zip -v myfile.zip t.*

  adding: t.md  (in=8121) (out=1051) (deflated 87%)

  adding: t.php (in=740) (out=319) (deflated 57%)

  adding: t.php.zip     (in=1666) (out=1666) (stored 0%)

total bytes=10527, compressed=3036 -> 71% savings

# 测试压缩包完整性

$ zip -T myfile.zip 

test of myfile.zip OK

# 测试压缩包文件内容

$ unzip -t myfile.zip 

Archive:  myfile.zip

    testing: t.md                     OK

    testing: t.php                    OK

    testing: t.php.zip                OK

No errors detected in compressed data of myfile.zip.

# 查看压缩包里内容

$ unzip -l myfile.zip 

Archive:  myfile.zip

  Length      Date    Time    Name

---------  ---------- -----   ----

     8121  06-08-2016 17:03   t.md

      740  06-08-2016 17:02   t.php

     1666  07-30-2016 17:38   t.php.zip

---------                     -------

    10527                     3 files

# 从压缩包里删除文件t.php.zip   

$ zip -d myfile.zip t.php.zip

deleting: t.php.zip

# 从压缩包里删除文件t.php

$ zip -d myfile.zip t.php

deleting: t.php

# 添加文件到压缩包里

$ zip -u myfile.zip t.php

  adding: t.php (deflated 57%)

# 给压缩包添加注释  

$ zip -z myfile.zip

enter new zip file comment (end with .):

test

.

# 查看压缩包注释

$ unzip -z myfile.zip 

Archive:  myfile.zip

test

# 解压到指定文件夹

$ unzip myfile.zip -d my

Archive:  myfile.zip

test .

  inflating: my/t.md                 

  inflating: my/t.php

# 排除文件不解压

$ unzip myfile.zip  -x t.php -d my

Archive:  myfile.zip

test .

  inflating: my/t.md

gz

格式：



gzip [options] 待压缩源文件

gunzip [options]  待解压文件

不用写最终的压缩文件名，会自动在后面加.gz后缀，同时删除源文件。

常用命令：













# 压缩1.log，同时会自动删除源文件

gzip 1.log

# 解压1.log.gz，同时会自动删除压缩包

gzip -d 1.log.gz

# 压缩1.log，保留源文件

gzip -k 1.log

# 解压1.log.gz，保留压缩包

gzip -dk 1.log.gz

# 查看压缩包信息

gzip -l 1.log.gz

# 递归的对目录里的每个文件单独压缩

gzip -r mydir

注意：gunzip与gzip -d等效，都可以解压gz文件。

更多参数：




-c, --stdout 将压缩后的内容在标准输出显示出来，保留原文件

-1, --fast 更快的压缩速度

-9, --best 更好的压缩率

示例：



# 压缩1.log为1.log.gz，保留源文件

gzip -c 1.log > 1.log.gz

bz2

格式：



bzip2 [options] 待压缩源文件

bunzip2 [options]  待解压文件

常用命令：









# 压缩1.log

bzip2 1.log

bzip2 -k 1.log

# 解压1.log.bz2

bzip2 -d 1.log.bz2

bzip2 -dk 1.log.bz2

bunzip2 1.log.bz2

bunzip2 -k 1.log.bz2

更多参数：




-c, --stdout 将压缩后的内容在标准输出显示出来，保留原文件

-1, --fast 更快的压缩速度

-9, --best 更好的压缩率

tar

格式：


tar [options] 目标压缩包名称 待压缩源文件

常用命令：




















# 打包后，以gzip 压缩

tar zcvf test.tar.gz /test  #压缩/test为test.tar.gz

# 解压test.tar.gz

tar zxvf test.tar.gz 

# 打包后，以bzip2 压缩

tar jcvf test.tar.bz2 /test  #压缩/test为test.tar.bz2

# 解压test.tar.bz2

tar jxvf test.tar.bz2

# 仅打包，不压缩

tar cvf test.tar /test  #压缩/test为test.tar

# 解压test.tar

tar xvf test.tar

# 查看压缩包内容列表

tar tvf test.tar.gz

# 解压到指定文件夹（目标文件夹必须存在）

$ tar -zxvf all.tar.gz -C my/

# 压缩时排除某些目录

$ tar -zcvf tomcat.tar.gz --exclude=tomcat/logs tomcat

$ tar -zcvf tomcat.tar.gz --exclude=tomcat/logs --exclude=tomcat/libs --exclude=tomcat/xiaoshan.txt tomcat

常用参数说明：








-c, --create: 建立压缩档案

-x, --extract, --get：解压

-t, --list：查看内容

-r, --append：向压缩归档文件末尾追加文件

-u, --update：更新原压缩包中的文件

-d, --diff, --compare 将压缩包里的文件与文件系统进行对比

    --delete 从压缩包里删除

这几个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的:







-z, --gzip, --gunzip, --ungzip：有gzip属性的

-j, --bzip2：有bz2属性的

-Z, --compress, --uncompress：有compress属性的

-v, --verbose：显示所有过程

-O, --to-stdout：将文件解开到标准输出

-C, --directory=DIR：解压到指定文件夹

最后的参数-f是必须的:


-f, --file=ARCHIVE: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。

查看命令帮助：




tar --help

tar -?

tar --usage

更多示例：














# 比较压缩包里文件与源文件变动

$ tar --diff -vf 1.log.tar 1.log

1.log

1.log: Mod time differs

1.log: Size differs

# 删除压缩包里的1.log

$ tar --delete -vf 1.log.tar 1.log

# 向压缩归档文件里追加文件

$ tar rvf 1.log.tar 1.log 2.log

1.log

2.log

# 向压缩归档文件里更新文件

$ tar uvf 1.log.tar 1.log 2.log

说明：不能向tar.gz和tar.bz2里追加或者更新文件：




$ tar zrvf all.tar.gz 3.log

tar: Cannot update compressed archives

Try 'tar --help' or 'tar --usage' for more information.

以上就是Linux压缩命令（总结）的详细内容，更多请关注php中文网其它相关文章！