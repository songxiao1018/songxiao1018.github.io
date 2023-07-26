---
title: python发送邮件
date: 2022-10-14 17:41:47
tags: python
categories: 学习
---



```
#!/usr/bin/python3
#-*- coding: utf-8 -*-            # 使其支持中文字符

import smtplib                    # 调用模块
from email.header import Header
from email.mime.text import MIMEText

#第三方SMTP服务
host = "smtp.163.com"          # 邮箱服务host = "smtp.yeah.net"
port = 465                     # 端口号port = 465
user = "xxxxxxxx@163.com"      # 用户名user = "XXXXXXXXXX@yeah.net"
password = "xxxxxxxxxxx"       # 授权码
sender = "xxxxxxxxxxxx@163.com"   # 发件人
receivers = ["xxxxxx@163.com",'xxxxxx@163.com','xxxxxx@163.com',"xxxxxx@163.com","xxxxxx@163.com","xxxxxx@163.com"]  # 收件人，可以群发邮件，多个用户名就以列表形式展现                                                      

content = '''                    
    这是一封测试邮件
    内容随你喜欢
    随便写
'''                         # 邮件内容
subject = '测试邮件'         # 邮件主题

#发送邮件
def send_email():
    msg = MIMEText(content+'\n send_email' ,'plain' ,'utf-8')
    msg['From'] = user
    msg['To'] = ','.join(receivers)        # 群发邮件形式，如果单独发送邮件直接调用receivers即可
    msg['Subject'] = subject+' send_email'


    try:
        #验证
        smtpObj = smtplib.SMTP_SSL(host,port)  # 启用SSL发短信
        smtpObj.login(user,password)           # 用户名密码验证
        smtpObj.sendmail(sender,receivers,msg.as_string())   # 发送
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)

if __name__ == '__main__':
    send_email()

```










提前准备，需要设置邮箱服务器


发送邮件代码块如下

#coding:utf-8

#发送邮件的
import smtplib
from email.mime.text import MIMEText
class SendEmail:
    global send_user
    global email_host
    global password
    email_host="smtp.qq.com"
    send_user="xxx@qq.com"
    password="xxx"
    #接受人，主题，内容
    def send_mail(self,user_list,sub,content):
        #发件者
        user="cherish"+"<"+send_user+">"
        #内容、格式、编码
        message=MIMEText(content,_subtype='plain',_charset='utf-8')
        #主题
        message['Subject']=sub
        #发送人
        message['From']=user
        #接受人
        message['To']=";".join(user_list)
        #服务连接
        server=smtplib.SMTP()
        server.connect(email_host)
        #邮件登录
        server.login(send_user,password)
        #发送邮件内容
        server.sendmail(user,user_list,message.as_string())
        #关掉连接
        server.close()
    def send_main(self,pass_list,fail_list):
        pass_num=float(len(pass_list))
        fail_num=float(len(fail_list))
        count_num=pass_num+fail_num
        #取小数后2位,通过率
        pass_result="%.2f%%"%(pass_num/count_num*100)
        fail_result = "%.2f%%"%(fail_num / count_num * 100)
        user_list = ['xx@qq.com','xx@qq.com']
        sub = "接口自动化测试报告"
        content="这次一共测试%s个接口,通过个数为%s,失败个数为%s,通过率为%s,失败率为%s"%(count_num,pass_num,fail_num,pass_result,fail_result)
        self.send_mail(user_list,sub,content)

if __name__ == '__main__':
    sen=SendEmail()
    sen.send_main([1,2,3,4],[5])


测试结果：

测试用例执行代码块

#coding:utf-8
from base.runmethod import RunMethod
from data.get_data import GetData
from data.depend_data import DependData
from util.operation_json import OperationJson
from util.common_util import CommonUtil
import operator
import json
from logs.get_log import get_log
from util.send_email import SendEmail
import getcwd
class RunTest:
	def __init__(self):
		self.path = getcwd.get_cwd()
		self.log_msg = get_log(self.path + '/data/get_data.py')
		self.run_method = RunMethod()
		self.data = GetData()
		self.com_util = CommonUtil()
		self.op_json = OperationJson('../dataconfig/rigang_data/header_value.json')
		self.json_path='../dataconfig/rigang_data/expect_monitor_add.json'

	#程序执行的
	def go_on_run(self):
		res = None
		pass_count = []
		fail_count = []
		#10  0,1,2,3
		#用例行数
		rows_count = self.data.get_case_lines()
		#遍历所有用例进行测试
		for i in range(1,rows_count):
			is_run = self.data.get_is_run(i)
			if is_run:
				caseid=self.data.get_caseid(i)
				url = self.data.get_request_url(i)
				method = self.data.get_request_method(i)
				request_data = json.dumps(self.data.get_data_for_json(i))
				expect = self.data.get_expect_data_for_json(i,self.json_path)
				header = self.data.is_header(i)
				depend_case=self.data.is_depend(i)
				#判断是否有数据依赖
				if depend_case!=None:
					self.depend_data = DependData(caseid)
					#获取依赖的响应数据
					depend_response_data=self.depend_data.get_data_for_key(i)
					#获取依赖字段
					depend_key=self.data.get_depend_field(i)
					#请求数据的依赖字段重新赋值之前的依赖数据
					request_data[depend_key]=depend_response_data
				# res = self.run_method.run_main(method, url, request_data)

				if header == '5':
					#根据关键字test获取header信息
					header = self.op_json.get_data('monitor_add')
					res = self.run_method.run_main(method,url,request_data,header)

					self.log_msg.info('该条用例header内容是：%s' % header)
					#将返回结果写入json文件
					response_dato_tojson=self.op_json.write_data(res,'../dataconfig/rigang_data/actual_monitor_add.json')
				else:
					res = self.run_method.run_main(method,url,request_data)
					response_dato_tojson=self.op_json.write_data(res, '../dataconfig/rigang_data/actual_monitor_add.json')
				read_json_data=self.op_json.read_data('../dataconfig/rigang_data/actual_monitor_add.json')
				self.log_msg.info('写入json的返回结果是：%s' % read_json_data)

				if operator.eq(expect,res) == True:
					self.data.write_result(i,'pass')
					#统计通过个数
					pass_count.append(i)
					self.log_msg.info('用例ID为%s-------------------测试通过\n'%caseid )
				else:
					res = json.dumps(res)
					self.data.write_result(i,res)
					#统计失败个数
					fail_count.append(i)
					self.log_msg.info('用例ID为%s-------------------测试失败\n' % caseid)

		send_email=SendEmail()
		send_email.send_main(pass_count,fail_count)

if __name__ == '__main__':
	run = RunTest()
	run.go_on_run()




测试结果

