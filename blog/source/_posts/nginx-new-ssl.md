---
title: nginx创建HTTPS连接new_ssl
date: 2022-10-14 11:23:04
tags: nginx
categories: 
    - 系统
---

创建存放SSL证书文件的文件夹：
$ sudo mkdir -p /etc/nginx/ssl

我这里是把这两个文件放在 /etc/nginx/ssl目录下，这里需要记住上传SSL证书文件的路径。
接着，我们需要给nginx的配置文件加上添加证书的路径以及开启安全证书，进入默认的配置文件：

$ vim /etc/nginx/sites-available/default

添加的内容如下：

点击 i ，进行修改内容，把以下内容复制/输入进去，当然别忘了把ssl_certificate和ssl_certificate_key后面路径的****换成是你的文件名字哦：
        listen 443 ssl;
        ssl_certificate    /etc/nginx/ssl/****.pem;
        ssl_certificate_key /etc/nginx/ssl/****.key;
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;

最后按esc退出，然后输入**:wq** 保存并退出。

然后检查一下我们修改内容有没有出错，输入：

$ nginx -t

提示successful


最后的最后，还需要重启一下nginx，不然的话是不会生效的。
输入：

$ sudo service nginx restart

最后，在浏览器访问我的域名，可以看到提示连接是安全的
