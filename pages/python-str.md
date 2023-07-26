---
title: python字符串处理
date: 2022-10-14 17:27:24
tags: python
categories: 学习
---
str='python String function'

生成字符串变量str='python String function'

字符串长度获取：len(str)
例：print '%s length=%d' % (str,len(str))

一、字母处理
全部大写：str.upper()
全部小写：str.lower()
大小写互换：str.swapcase()
首字母大写，其余小写：str.capitalize()
首字母大写：str.title()
print '%s lower=%s' % (str,str.lower())
print '%s upper=%s' % (str,str.upper())
print '%s swapcase=%s' % (str,str.swapcase())
print '%s capitalize=%s' % (str,str.capitalize())
print '%s title=%s' % (str,str.title()) 
二、格式化相关
获取固定长度，右对齐，左边不够用空格补齐：str.ljust(width)
获取固定长度，左对齐，右边不够用空格补齐：str.ljust(width)
获取固定长度，中间对齐，两边不够用空格补齐：str.ljust(width)
获取固定长度，右对齐，左边不足用0补齐
print '%s ljust=%s' % (str,str.ljust(20))
print '%s rjust=%s' % (str,str.rjust(20))
print '%s center=%s' % (str,str.center(20))
print '%s zfill=%s' % (str,str.zfill(20))

三、字符串搜索相关
搜索指定字符串，没有返回-1：str.find('t')
指定起始位置搜索：str.find('t',start)
指定起始及结束位置搜索：str.find('t',start,end)
从右边开始查找：str.rfind('t')
搜索到多少个指定字符串：str.count('t')
上面所有方法都可用index代替，不同的是使用index查找不到会抛异常，而find返回-1
print '%s find nono=%d' % (str,str.find('nono'))
print '%s find t=%d' % (str,str.find('t'))
print '%s find t from %d=%d' % (str,1,str.find('t',1))
print '%s find t from %d to %d=%d' % (str,1,2,str.find('t',1,2))
#print '%s index nono ' % (str,str.index('nono',1,2))
print '%s rfind t=%d' % (str,str.rfind('t'))
print '%s count t=%d' % (str,str.count('t'))

三、字符串替换相关
替换old为new：str.replace('old','new')
替换指定次数的old为new：str.replace('old','new',maxReplaceTimes)
print '%s replace t to *=%s' % (str,str.replace('t', '*'))
print '%s replace t to *=%s' % (str,str.replace('t', '*',1))

四、字符串去空格及去指定字符
去两边空格：str.strip()
去左空格：str.lstrip()
去右空格：str.rstrip()
去两边字符串：str.strip('d')，相应的也有lstrip，rstrip
str=' python String function '
print '%s strip=%s' % (str,str.strip())
str='python String function'
print '%s strip=%s' % (str,str.strip('d'))

按指定字符分割字符串为数组：str.split(' ')

五、默认按空格分隔
str='a b c de'
print '%s strip=%s' % (str,str.split())
str='a-b-c-de'
print '%s strip=%s' % (str,str.split('-'))

六、字符串判断相关
是否以start开头：str.startswith('start')
是否以end结尾：str.endswith('end')
是否全为字母或数字：str.isalnum()
是否全字母：str.isalpha()
是否全数字：str.isdigit()
是否全小写：str.islower()
是否全大写：str.isupper()
str='python String function'
print '%s startwith t=%s' % (str,str.startswith('t'))
print '%s endwith d=%s' % (str,str.endswith('d'))
print '%s isalnum=%s' % (str,str.isalnum())
str='pythonStringfunction'
print '%s isalnum=%s' % (str,str.isalnum())
print '%s isalpha=%s' % (str,str.isalpha())
print '%s isupper=%s' % (str,str.isupper())
print '%s islower=%s' % (str,str.islower())
print '%s isdigit=%s' % (str,str.isdigit())
str='3423'
print '%s isdigit=%s' % (str,str.isdigit())