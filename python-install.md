---
title: linux下载和安装python
date: 2022-08-18 15:23:09
tags: 
    - python
    - linux
categories: 系统
---

# Debian系统 安装Python

> 本文参考自[Python入门：在Debian系统安装Python 3](https://cloud.tencent.com/developer/article/1165255)

## 介绍

> Python是一种面向对象的解释型计算机程序设计语言，由荷兰人Guido van Rossum于1989年发明，第一个公开发行版发行于1991年。 可用于许多不同的编程项目。这个名字的灵感源自英国喜剧组织Monty Python，开发团队希望让Python成为一种有趣的语言，并于1991年首次发布。Python易于设置，编写方式相对简单，并及时反馈错误，是初学者和经验丰富的开发人员的绝佳选择。Python 3是该语言的最新版本。

> 本教程将指导您在本地Linux机器上安装Python 3并通过命令行设置编程环境。本教程将介绍Debian 8的安装过程，原理适用于Debian Linux的任何其他发行版。

## 准备

> 1. Debian 8或其他版本的Debian Linux的计算机（服务器）

### 第一步 - 安装Python 3

> 我们将在命令行上完成安装和设置，这是一种与计算机交互的非图形方式。也就是说，您不是点击按钮，而是输入文本并通过文本从计算机接收反馈。命令行（也称为shell）可以帮助您修改和自动化您每天在计算机上执行的许多任务，是软件开发人员必不可少的工具。您可以学习许多终端命令，可以让您做更强大的事情。

> Debian 8和其他版本的Debian Linux都预装了Python 3和Python 2。为了确保我们的版本是最新的，让我们用apt-get更新和升级系统：

```
sudo apt-get update
sudo apt-get -y upgrade
```

> -y将确认我们同意所有要安装的项目，但根据您的Linux版本不同，您可能需要确认其他提示作为系统更新和升级。

>完成该过程后，我们可以通过输入以下内容来检查系统中安装的Python 3的版本：

```
python3 -V
```

> 您将在终端窗口中收到输出，告知您Python版本号。版本号可能会有所不同，像这样：`Python 3.9.0`

> 让我们安装pip管理Python的软件包：

```
sudo apt-get install -y python3-pip
```

> pip是一个与Python一起使用的工具，主要用于安装和管理我们可能想要在我们的开发项目中使用的编程包。您可以输入以下命令安装Python包：

```
pip3 install package_name
```

> package_name可以指代任何Python包或库，例如用于Web开发的Django或用于科学计算的NumPy。因此，如果您想安装NumPy，可以使用pip3 install numpy命令执行此操作。

> 还有一些软件包和开发工具可以安装，以确保我们为编程环境提供强大的设置，命令如下：

```
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```

### 第二步 - 设置虚拟环境

> 设置了Python，并安装了pip和其他工具后，我们就可以为我们的开发项目设置一个虚拟环境。

> 虚拟环境使您可以在计算机上为Python项目创建一个隔离空间，确保每个项目都有自己的一组依赖项，这些依赖项不会破坏任何其他项目。

> 设置编程环境使我们能够更好地控制Python项目以及如何处理不同版本的包。在使用第三方软件包时，这一点尤为重要。

> 您可以根据需要设置尽可能多的Python编程环境。每个环境基本上都是计算机中的一个目录或文件夹，其中包含一些脚本以环境运行。

> 首先，我们需要安装venv模块，它是Python 3库的一部分，以便我们可以为我们创建虚拟环境。我们输入以下命令安装venv：

```
sudo apt-get install -y python3-venv
```

> 安装完成后，我们就可以创建环境了。让我们选择我们想要放入Python编程环境的目录，或者我们可以用mkdir创建一个新目录，如：

```
mkdir environments
cd environments
```

> 进入您希望环境保存的目录后，可以通过运行以下命令来创建环境：

```
python3 -m venv my_env
```

> 这会设置一个新目录，其中包含一些我们可以用ls命令查看的项目：

```
ls my_env
```

> `bin  include  lib  lib64  pyvenv.cfg`这些文件一起用于确保您的项目与本地计算机的隔离，以便系统文件和项目文件不会混合。这是版本控制的一个好例子，并确保您的每个项目都可以访问所需的特定软件包。Python Wheels是Python的内置包格式，可以通过减少编译所需的次数来加速软件生产。你会在每个lib目录中找到它。

> 要使用此环境，您需要激活它，您可以通过输入以下调用activate脚本的命令来执行此操作：

```
source my_env/bin/activate
```

> 您的提示现在将以您的环境名称为前缀，在这里是my_env。根据您运行的Debian Linux的版本不同，您的前缀可能看起来有所不同，他们看起来应该是这样子的：

```
(my_env) sammy@sammy:~/environments$
```

> 这个前缀让我们知道环境当前是my_env在运行的，这意味着当我们在这里创建程序时，它们将只使用这个特定环境的设置和包。

> 注意：在虚拟环境中，您可以使用python代替python3，pip代替pip3。如果在环境之外使用Python 3，则需要专门使用python3和pip3。

> 执行这些步骤后，您的虚拟环境即可使用。

### 第3步 - 离开虚拟环境

> 要离开环境，只需输入命令`deactivate`，您将返回到原始目录。

## 结论

> 恭喜！此时，您已经学会了如何设置了Python 3编程环境，可以开始编写项目啦！更多Python教程请关注腾讯云+社区。

####参考文献：《How To Install Python 3 and Set Up a Local Programming Environment on Debian 8》