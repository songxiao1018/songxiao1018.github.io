---
title: windows系统修改键位
date: 2022-11-06 00:10:42
tags: 
   - windows
   - python
categories: 
   - 系统
---
不知道大家生活中有没有遇到这些情况：键盘上某个比较重要的键损坏或失灵而要重新更换键盘，或者在一些游戏、办公软件重的一些默认按键不合理，又或者希望自己DIY出一套属于自己的键位布局。那么我想这篇文章对你会很有帮助。

前几个月因心血来潮想尝试一些其他键位布局（例如Dvorak、Norman、Colemak等），需要修改键盘键位。其实，修改键位的方法也有很多，比较常见的是安装第三方辅助软件修改键位映射和功能。但对于我个人来说，出于简洁安全、自由可控的原因，不太喜欢在自己计算机上安装一些不必要的软件，这个功能完全可以在Windows上通过修改底层的注册表实现。

先说一下这篇文章的大致内容：

实现原理
自制管理工具（Python3）


实现原理



在Windows注册表中有个"Scancode Map"(即扫描码映射)的键，我们可以通过修改这个键的值来实现键位映射的更改。



"Scancode Map"的值的格式是"hex:00,00,00,00,00,00,00,00,xx,00,00,00,[yy,yy,yy,yy,...,yy,yy,yy,yy,]00,00,00,00"

前8个16进制的值（即前8组00）表示版本号和头部字节，后4个16进制的值（即最后的4组00）表示结束标志，中间xx表示映射数目，最小值为01（考虑到结束标志的4组00）,中括号内为可写项，也是我们修改键位比较关键的部分，每四个代表一组映射。

在我们键盘上每一个按键都有其十六进制扫描码，例如A的扫描码为"1e",其十六进制扫描码修正形式（为了表示方便就这么说吧）就是"001e",B的扫描码为"0030",右ctrl键的扫描码为"e01d",右alt键的扫描码则表示为"e038"，空值的扫描码为"0000"（可实现无效按键或者说是屏蔽按键）。具体其他按键扫描码在源码中贴有。

既然我们知道键盘上每一个键都具有其对应的扫描码，那么我们假设需要A和B键互换，应该怎么做呢？这个时候就需要我们向中括号中添加我们需要的值，"30,00,1e,00,"就可以实现将B键的功能映射到物理键盘A上（通俗点说就是敲击键盘上的A键会打出B字符，同时要注意值的顺序）。你以为这样就完了吗？不然。"30,00,1e,00,"只能将B键功能映射在物理键盘A键位上，而物理键位B键并未被映射成A！这很危险，相当于键盘上没有一个按键能实现A的功能，所以我们还得添加一项"1e,00,30,00,"。最后我们的"Scancode Map"的完整值就为"hex:00,00,00,00,00,00,00,00,03,00,00,00,30,00,1e,00,1e,00,30,00,00,00,00,00"。就这一串值就可完全调换A，B键的功能。

再来一个，我们要实现右Alt键能实现右Ctrl键的功能，并且屏蔽掉右Ctrl键，那么其"Scancode Map"值就为"hex:00,00,00,00,00,00,00,00,03,00,00,00,1d,e0,38,e0,00,00,1d,e0,00,00,00,00"。



那么问题来了，既然我知道这个键位和所谓的键盘扫描码之间的对应关系和Scancode值之后，具体怎么实现呢？



别急，我们一步步来，先打开Windows注册表编辑器（在cmd或powershell命令行下键入regedit回车即可打开），然后在"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layout"这个项下新建一个名为"ScanCode Map"键（右键新建二进制值），然后再右键名称列下的这个"ScanCode Map"修改，这时就可以依次键入编辑那一串hex值了，最后确定就完成了注册表的修改了！



图示如下，先新建这个ScanCode Map的键（右键Keyboard Layout或空白处，然后选择新建二进制值）






然后修改值（我的这个hex值功能是实现左Ctrl和CapsLock互换，毕竟Emacs党）




但是，修改完了后并不能立即生效，因为是通过注册表修改底层键位映射所以需要重启计算机，重启资源管理器也是没有用的。



那么，要还原按键怎么办？也很简单，有两种方法，一是从注册表中删除你创建的ScanCode Map这个键，或者用"hex:00,00,00,00,00,00,00,00,01,00,00,00,00,00,00,00"覆盖掉原来的值就行了。



当然，如果修改的键位比较多的话，通过查各个键位映射值，修改注册表写hex值，就麻烦很多了（很佩服曾经的自己硬是这样写了一些键位布局）。这时我们需要一个工具来管理，可以用第三方软件。但是既然原理我们已经知道了，也并不难远未达到工程级的量级，那完全可以自己实现这个管理工具。我们可以用Java，C++，Python等来写，这不重要，自己喜欢什么就用什么吧。下面是我用Python写的一个布局管理工具。









自制管理工具



这个工具名为layout_manage.py，功能是实现将我们要修改的键位关系转换为hex，并导出bat或reg文件（bat是Windows批处理文件，reg是Windows注册表脚本文件，在这里的功能是将hex值写入前面注册表中"ScanCode Map"这个键中）到layout_bat或layout_reg文件夹中。其本身不带有修改注册表功能（python自身的权限问题），只是生成的文件具有此功能。

即我们想修改以下键位：将qwer和asdf调换位置，小键盘123和789调换位置，屏蔽右shift键。这时我们只需要新建一个文本文件（例如一个名为test.txt的文件），将以下内容写入：




这个文件内容是按键值对组成的，"Q: A"的意思是将物理按键Q映射为A字符，即按Q键敲出A，更容易让人理解，冒号前为物理按键，冒号后为按键功能。说一下这个格式规则：

忽略大小写
忽略换行符、冒号、分号前后的空白字符（位于两单词间的空格不忽略，如Left Ctrl中间只能有一个空格）
小键盘上的字符前需要加n，例如小键盘上的'0'和'.'应分别写为"n0"和'n.'
一些功能键需正确写入，如：Tab、Esc、CapsLock、Backspace、Delete、Enter、Left Ctrl、Left Windows等
然后我们将这个文件作为参数，传递给layout_manage.py并执行。有两种方法，第一种是直接拖动这个txt文件到layout_manage.py图标上，这样layout_manage.py也能顺利执行。第二种方法是在cmd或powershell中执行命令"python layout_manage.py test.txt",注意路径问题。

此外如果没有其他参数传递给该脚本文件时（即双击直接执行），将会生成一个recover文件，即还原初始键位的文件，也很方便。



附上源码，注释应该很清楚了：

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import os

save_format = "reg"    #这个值可以修改，有两个选项(bat和reg)，可选择生成bat批处理文件或者reg注册表脚本文件,功能一样

class CountError(Exception):    #文本文件格式错误异常
    pass

class FileFormatError(Exception):    #save_format值异常
    pass


if save_format not in ["bat","reg"]:
    raise FileFormatError("The variable 'save_format'`s value must be 'bat' or 'reg'.")


if __name__ == "__main__":
    
    if not os.path.isdir("layout_"+save_format):
        os.mkdir("layout_"+save_format)

    if len(sys.argv) == 1:
        if save_format == "bat":
            with open("layout_bat/recover.bat",'w', encoding="utf-8") as f:
                f.write('@echo off\nreg delete "hklm\\system\\currentcontrolset\\control\\keyboard layout" /v "ScanCode Map" /f\necho "键位已恢复，重启系统后生效"\npause')
            input("恢复文件recover.bat已生成至layout_bat文件夹下，以管理员身份右键执行该文件后重启系统生效。\n按回车键退出程序...")

        else:
            with open("layout_reg/recover.reg",'w', encoding="utf-8") as f:
                f.write('Windows Registry Editor Version 5.00\n[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Keyboard Layout]\n"ScanCode Map"=hex:00,00,00,00,00,00,00,00,01,00,00,00,00,00,00,00')
            input("恢复文件recover.reg已生成至layout_reg文件夹下，双击执行该文件后重启系统生效。\n按回车键退出程序...")

    elif len(sys.argv) == 2:
        scan_code_dict = {
            "00 00":"None",
            "01 00":"Esc",    #即Esc键的扫描码是"0001"
            "02 00":"1",
            "03 00":"2",
            "04 00":"3",
            "05 00":"4",
            "06 00":"5",
            "07 00":"6",
            "08 00":"7",
            "09 00":"8",
            "0a 00":"9",
            "0b 00":"0",
            "0c 00":"-",
            "0d 00":"=",
            "0e 00":"Backspace",
            "0f 00":"Tab",
            "10 00":"Q",
            "11 00":"W",
            "12 00":"E",
            "13 00":"R",
            "14 00":"T",
            "15 00":"Y",
            "16 00":"U",
            "17 00":"I",
            "18 00":"O",
            "19 00":"P",
            "1a 00":"[",
            "1b 00":"]",
            "1c 00":"Enter",
            "1d 00":"Left Ctrl",
            "1e 00":"A",
            "1f 00":"S",
            "20 00":"D",
            "21 00":"F",
            "22 00":"G",
            "23 00":"H",
            "24 00":"J",
            "25 00":"K",
            "26 00":"L",
            "27 00":"Semicolon",    #由评论区指出，键盘上的“;”应该用其他值代替，否则会与配置文本文件中的“;”混淆
            "28 00":"'",
            "29 00":"`",
            "2a 00":"Left Shift",
            "2b 00":"\\",
            "2c 00":"Z",
            "2d 00":"X",
            "2e 00":"C",
            "2f 00":"V",
            "30 00":"B",
            "31 00":"N",
            "32 00":"M",
            "33 00":",",
            "34 00":".",
            "35 00":"/",
            "36 00":"Right Shift",
            "37 00":"n*",
            "38 00":"Left Alt",
            "39 00":"Space",
            "3a 00":"Caps Lock",
            "3b 00":"F1",
            "3c 00":"F2",
            "3d 00":"F3",
            "3e 00":"F4",
            "3f 00":"F5",
            "40 00":"F6",
            "41 00":"F7",
            "42 00":"F8",
            "43 00":"F9",
            "44 00":"F10",
            "45 00":"Num Lock",
            "46 00":"Scroll Lock",
            "47 00":"n7",
            "48 00":"n8",
            "49 00":"n9",
            "4a 00":"n-",
            "4b 00":"n4",
            "4c 00":"n5",
            "4d 00":"n6",
            "4e 00":"n+",
            "4f 00":"n1",
            "50 00":"n2",
            "51 00":"n3",
            "52 00":"n0",
            "53 00":"n.",
            "57 00":"F11",
            "58 00":"F12",

            
            "1c e0":"nEnter",
            "1d e0":"Right Ctrl",
            "37 e0":"PrtSc",
            "38 e0":"Right Alt",
            "47 e0":"Home",
            "48 e0":"Up",
            "49 e0":"Page Up",
            "4b e0":"Left",
            "4d e0":"Right",
            "4f e0":"End",
            "50 e0":"Down",
            "51 e0":"Page Down",
            "52 e0":"Insert",
            "53 e0":"Delete",
            "5b e0":"Left Windows",
            "5c e0":"Right Windows",
            }

        fun_key_dict = dict((m.upper(),n) for n,m in scan_code_dict.items())    #键值互换,键值全大写
        content = '00 00 00 00 00 00 00 00'
        
        #用于暂时保存映射前后的键位，判断这次键位修改是否有风险
        before_map_set = set()
        after_map_set = set()

        with open(sys.argv[1], encoding="utf-8") as f:
            p = f.read().strip().split(';')
            p.remove('')
            content += ' {:0>2x} 00 00 00'.format(len(p)+1)
            try:
                for i in p:
                    if len(i.strip().split(':')) == 2:
                        before_map_set.add(i.split(':')[0].strip().upper())
                        after_map_set.add(i.split(':')[1].strip().upper())
                        content += ' '+fun_key_dict[i.split(':')[1].strip().upper()]+' '+fun_key_dict[i.split(':')[0].strip().upper()]
                    else:
                        raise CountError
                content += ' 00 00 00 00'
            except KeyError:
                print("文件中键名称有误")
                
            except CountError:
                print("文件中未按格式书写")
            else:
                if before_map_set != after_map_set:
                    run = input("此次键位替换存在风险，{}键功能将在键盘上无对应按键，是否继续？(输入y继续，否则退出程序)".format(str(before_map_set-after_map_set)[1:-1]))
                    if run != 'y':
                        sys.exit()

                if save_format == "bat":
                    with open("layout_bat/"+'.'.join(sys.argv[1].split('\\')[-1].split('.')[:-1])+'.bat','w', encoding="utf-8") as g:
                        g.write('@echo off\nreg add "hklm\\system\\currentcontrolset\\control\\keyboard layout" /v "ScanCode Map" /t REG_BINARY /d "{}" /f\necho "键位已完成修改，重启系统后生效"\npause'.format(''.join(content.split())))
                    input("...\n{}文件已生成至layout_bat目录下，右键以管理员身份执行该文件后重启系统生效。\n按回车键退出程序...".format('.'.join(sys.argv[1].split('\\')[-1].split('.')[:-1])+'.'+save_format))

                else:
                    with open("layout_reg/"+'.'.join(sys.argv[1].split('\\')[-1].split('.')[:-1])+'.reg','w', encoding="utf-8") as g:
                        g.write('Windows Registry Editor Version 5.00\n[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Keyboard Layout]\n"ScanCode Map"=hex:{}'.format(','.join(content.split())))

                    input("...\n{}文件已生成至layout_reg目录下，双击执行该文件后重启系统生效。\n按回车键退出程序...".format('.'.join(sys.argv[1].split('\\')[-1].split('.')[:-1])+'.'+save_format))
    else:
        input("传入参数错误，按回车键退出程序...")


另外通过此脚本生成的bat或reg文件可以将其保存好，在其他Windows系统电脑上可以直接执行并修改为你想要的键位，这样可以一次生成，多处适用！切勿用来恶作剧哦。

关于键位布局：我用了一个多月的Dvorak和两个多月的Norman，刚开始练习使用新键位的一周非常痛苦和新鲜，适应之后在英文文章输入的确要快点，但不是很明显。如果是敲code的话，就没什么可比性了。考虑到种种因素（尤其是在用其他人设备时），所以最后还是回归了QWERTY键位。

编辑于 2020-11-13 16:14



https://zhuanlan.zhihu.com/p/29581818
