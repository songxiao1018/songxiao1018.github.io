---
title: nginx-ip
date: 2022-12-21 11:25:35
categories:
tags:
---
https://www.jianshu.com/p/4e761ec96f67

Nginx 多个子域名映射到不同的端口或 ip

MrTricker
IP属地: 福建
0.267
2019.07.17 15:42:10
字数 1,163
阅读 7,597
场景介绍

在部署 DevOps 环境时，多个服务通过 Docker 部署到一个服务器上，映射到不同的端口。
现在每次访问，都要带上端口号，既不美观，也很麻烦。

一、思考过程
如果不想带上端口号，就只能访问 80 或 443 端口。
可以用过二级目录区分服务，通过反向代理转发到不同的 Server。
可以用过子域名区分服务，通过反向代理转发到不同的 Server。
二、方案评估
对于不带端口号访问，以我目前的经验来看，找不到其它更好的方法，只能使用 80 或 443 端口。
使用二级目录区分服务，可行性很大。
能通过二级目录名，明确区分服务。
可是和直接使用端口号差别不大，只是把辨别服务的方法，从端口号变成了二级目录名。
可能导致 url 过长。
还是没有什么美观性。
使用子域名区分服务，可行性与二级目录相差无几。
能通过子域名，明确区分服务。
具有一定的美观性。
三、方案确定 和 方案设计
我决定采用采用 子域名区分服务 的方式，然后使用 nginx 做反向代理，分发到不同的端口。

1. 本地测试
注意

我使用的环境是 Ubuntu Desktop 桌面操作系统。

首先安装 nginx

# 使用 Ubuntu 包管理器中的 nginx 即可。
$ sudo apt update
$ sudo apt install nginx
安装 Docker 和 Docker Composer

参考官方文档 Get Docker CE for Ubuntu 和 Install Docker Compose。

创建目录结构

# 我使用的是 Jetbrains 全家桶；
# 这里比较麻烦。
$ mkdir -p DevOps
$ cd mkdir
$ mkdir -p gitlab registry teamcity mysql
$ mkdir -p -m 750 hub/backups hub/conf hub/data hub/logs youtrack/backups youtrack/conf youtrack/data youtrack/logs upsource/backups upsource/conf upsource/data upsource/logs
$ sudo chmod -R 13001:13001 hub youtrack upsource
$ touch docker-compose.yml
编写 docker-compose.yml 配置文件

version: '3'

services:

  gitlab:
    image: gitlab/gitlab-ce:latest
    restart: always
    hostname: 'gitlab.tricker.org'
    prots:
      - 8888:80
      - 2222:22
    volumes:
      - './gitlab/config:/etc/gitlab'
      - './gitlab/data:/var/opt/gitlab'
      - './gitlab/logs:/var/log/gitlab'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url "http://gitlab.tricker.org"
        gitlab_rails["gitlab_shell_ssh_port"] = 2222
    networks:
      devops:
        aliases:
          - 'gitlab.tricker.org'

  registry:
    image: registry:latest
    hostname: 'registry.tricker.org'
    ports:
      - 5555:5000
    volumes:
      - './registry/data:/var/lib/registry'
    networks:
      devops:
        aliases:
          - 'registry.tricker.org'

  hub:
    image: jetbrains/hub:2019.1.11584
    hostname: 'hub.tricker.org'
    ports:
      - 18080:8080
    volumes:
      - './hub/data:/opt/hub/data'
      - './hub/conf:/opt/hub/conf'
      - './hub/logs:/opt/hub/logs'
      - './hub/backups:/opt/hub/backups'
    networks:
      devops:
        aliases:
          - 'hub.tricker.org'

  youtrack:
    image: jetbrains/youtrack:2019.2.54193
    hostname: 'youtrack.tricker.org'
    ports:
      - 18081:8080
    volumes:
      - './youtrack/data:/opt/youtrack/data'
      - './youtrack/conf:/opt/youtrack/conf'
      - './youtrack/logs:/opt/youtrack/logs'
      - './youtrack/backups:/opt/youtrack/backups'
    networks:
      devops:
        aliases:
          - 'youtrack.tricker.org'
    depends_on:
      - hub

  upsource:
    image: jetbrains/upsource:2019.1.1432
    hostname: 'upsource.tricker.org'
    ports:
      - 18082:8080
    volumes:
      - './upsource/data:/opt/upsource/data'
      - './upsource/conf:/opt/upsource/conf'
      - './upsource/logs:/opt/upsource/logs'
      - './upsource/backups:/opt/upsource/backups'
    networks:
      devops:
        aliases:
          - 'upsource.tricker.org'
    depends_on:
      - hub
      - gitlab

  teamcity:
    image: jetbrains/teamcity-server
    hostname: 'teamcity.tricker.org'
    ports:
      - 18111:8111
    volumes:
      - './teamcity/data:/data/teamcity_server/datadir'
      - './teamcity/logs:/opt/teamcity/logs'
    networks:
      devops:
        aliases:
          - 'teamcity.tricker.org'
    depends_on:
      - mysql
      - gitlab

networks:
  devops:
修改 hosts 文件

# 注意: 这里一定要使用 root 权限。
$ sudo vim /etc/hosts
# 关于 vim 的使用，此处不再复述，有问题找百度。
127.0.0.1       gitlab.tricker.org
127.0.0.1       registry.tricker.org
127.0.0.1       hub.tricker.org
127.0.0.1       youtrack.tricker.org
127.0.0.1       upsource.tricker.org
127.0.0.1       teamcity.tricker.org
修改 nginx 配置

# 进入 nginx 文件夹，这个文件夹内的操作，几乎都需要 root 权限。
$ cd /etc/nginx
$ cd sites-available/
$ sudo mv default default.backup
$ sudo vim devops
server {
    listen 80;

    server_name gitlab.tricker.org;

    location / {
        proxy_pass       http://127.0.0.1:8888;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;

    server_name registry.tricker.org;

    location / {
        proxy_pass       http://127.0.0.1:5555;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;

    server_name hub.tricker.org;

    location / {
        proxy_pass       http://127.0.0.1:18080;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;

    server_name youtrack.tricker.org;

    location / {
        proxy_pass       http://127.0.0.1:18081;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;

    server_name upsource.tricker.org;

    location / {
        proxy_pass       http://127.0.0.1:18082;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;

    server_name teamcity.tricker.org;

    location / {
        proxy_pass       http://127.0.0.1:18111;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
# 重启 nginx 打开浏览器访问相应的子域名，就可以转到相应的服务了。
$ sudo systemct restart nginx