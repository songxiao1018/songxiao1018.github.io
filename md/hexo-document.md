---
title: 使用hexo搭建博客
date: 2022-08-19 15:23:09
tags: hexo
categories: 学习
---

# Hexo 使用方法

## 学习目标 

### 知识目标： 

1. 通过学习，了解博客搭建常用的几种方式以及之间的区别 
> 1. 第三方平台搭建 
> 1. 静态网站生成页面，搭配`Github`展示 
> 1. 管理系统`CMS`搭建 
> 1. 手写前后端代码 
2. 熟悉静态页面的生成技术 
3. 学会最基本的`git`操作 
 
### 能力目标： 
1. 实现个人博客的搭建 
2. 能熟练在`Github/Gitee`上部署页面 
 
---

## 学习流程 

---

### 1. 工具基本介绍 

#### 1. Hexo 介绍 

`Hexo`是一个快速、简单且功能强大的博客框架。你用`Markdown`（或其他标记语言）写帖子，`Hexo` 会在几秒钟内生成带有漂亮主题的静态文件。 

#### 2. Gitee 介绍 

码云`Gitee`是开源中国社区在 2013 年推出的基于`Git`的代码托管服务，专为开发者提供稳定、高效、安全的云端软件开发协作平台，无论是个人、团队、或是企业，都能够用`Gitee`实现代码托管、项目管理、协作开发，更有代码质量分析、项目演示等丰富功能。 

`Gitee`目前已经成为国内最大的代码托管平台，致力于为国内开发者提供优质稳定的托管服务，与 `GitHub`类似区别在于码云国内，`GitHub`国外。 

#### 3. Git 介绍 

`Git`是目前世界上最先进的分布式版本控制系统，可以有效、高速的处理从很小到非常大的项目版本管理。也就是用来管理你的`hexo`博客文章，上传到` GitHub `的工具。`Git `非常强大，我觉得建议每个人都去了解一下。 

#### 4. Node.js 介绍 

`Node.js `是一个能够在服务区端运行` JavaScript `的开放源代码、跨平台`JavaScript `运行环
境。 

`Hexo `是基于` node.js `编写的，所以需要安装一下` nodeJs `和里面的` npm `工具。 

---

### 2. 整体搭建流程 

---

### 开始搭建 
 1. 基础准备 
> 1. Gitee 的注册 

> 2. Git、Node.js 安装 

安装` Hexo `相当简单，只需要先安装下列应用程序即可：

> Node.js (Node.js 版本需不低于 10.13，建议使用 Node.js 12.0 及以上版本) 

```
Node.js 为大多数平台提供了官方的 安装程序。对于中国大陆地区用户，可以前往 淘宝 Node.js 镜像 下载。 

其它的安装方法： 
1. Windows：通过 nvs（推荐）或者 nvm 安装。 
2. Mac：使用 Homebrew 或 MacPorts 安装。 
3. Linux（DEB/RPM-based）：从 NodeSource 安装。 
4. 其它：使用相应的软件包管理器进行安装，可以参考由 Node.js 提供的 指导。 

对于 Mac 和 Linux 同样建议使用 nvs 或者 nvm，以避免可能会出现的权限问题。 

Windows 用户使用 Node.js 官方安装程序时，请确保勾选 Add to PATH 选项（默认已勾选） 
For Mac / Linux 用户如果在尝试安装 Hexo 的过程中出现 EACCES 权限错误，请遵循 由 npmjs 发布的指导 修复该问题。强烈建议 不要 使用 root、 sudo 等方法覆盖权限 
Linux 如果您使用 Snap 来安装 Node.js，在 初始化 博客时您可能需要手动在目标文件夹中执行 。 npm install 
```

> Git 

```
1. Windows：下载并安装 git. 
2. Mac：使用 Homebrew, MacPorts 或者下载 安装程序。 
3. Linux (Ubuntu, Debian)： 
sudo apt-get install git-core 
Linux (Fedora, Red Hat, CentOS)： 
sudo yum install git-core 

Mac 用户如果在编译时可能会遇到问题，请先到 App Store 安装 Xcode，Xcode 完成后，启动并进入 Preferences -> Download -> Command Line Tools -> Install 安装命令行工具。

Windows 用户对于中国大陆地区用户，可以前往淘宝 Git for Windows 镜像 下载 git 安装包。 查看下 Git、Node.js 版本，确保安装无误 git --version node -v和npm -v

 顺便说一下，windows 在 git 安装完后，就可以直接使用 git bash 来敲命令行了，不用自带的 cmd，cmd 有点难用。 
```

> 安装 Hexo 

```
进入 Hexo 的官网：Hexo就可以看到对于 Hexo 的详细介绍，直接下滑，然后点击 Get Started，即可进入 Hexo 使用介绍文档，也可以直接访问：https://hexo.io/docs/ 进入。 
```

---

### 正式开始搭建
---

所有必备的应用程序安装完成后，即可使用` npm `安装` Hexo`。 

* 首先我们需要新建一个项目目录，以我为例：我会在桌面的` Project `目录下新建一个` HexoBlog `文件夹用于存放改项目相关文件。
``` 
cd Desktop/Project/ 
mkdir HexoBlog&&cd HexoBlog npm install -g hexo-cli 
```

这个时候如果直接运行下面语句安装 Hexo，你可能会遇到`rollbackFailedOptional`。 
> 这是因为网络问题（npm 的服务器位于国外下载慢），可以使用 cnpm（淘宝团队做的国内镜像）的获取镜像或者直接修改 npm的资源获取地址为国内的。 

#### 解决方案

* 安装 cnmp 

```
npm install -g cnpm --registry=https://registry.npm.taobao.org 
```

* 直接修改 npm 资源获取地址（推荐） 

```
npm config set registry http://registry.npm.taobao.org 
```

可能出现的问题：[npm WARN config global `--global`, `--local` are deprecated. Use `--location=global` instead ](http://www.kuazhi.com/post/305594.html)

* 初始化一个 Hexo Blog 
> 前面已经准备好了所有相关环境，接下来我们就正式来初始化一个`Hexo`博客吧～初始化的命令格式为` hexo init <项目名称>`，这里我们暂且叫做` blog`。

```
hexo init blog 
```

* 新建完成后，指定文件夹目录下有：

```
:node_modules: 依赖包 
:public：存放生成的页面 
:scaffolds：生成文章的一些模板 
:source：用来存放你的文章 
:themes：主题 
:_config.yml: 博客的配置文件
```

* 初始化项目后，我们只需在本地执行下面命令即可在本地进行预览 

```
cd blog 
hexo s 
```

* 首先我们需要进入到新建的项目目录下，然后执行 hexo s 即可启动项目，然后我们访问[127.0.0.1:4000](127.0.0.1:4000)或者[http://localhost:4000/](http://localhost:4000/)即可查看网站啦～ 

