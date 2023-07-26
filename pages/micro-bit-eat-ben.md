---
layout: posts
title: micor：bit制作吃豆子小游戏
date: 2022-07-29 15:23:09
tags: micro:bit
categories: 学习
---

> 在 [https://songxiao1018.github.io/micro-bit-eat-ben/](https://songxiao1018.github.io/micro-bit-eat-ben/) 打开此页面

## 用作扩展

此仓库可以作为 **插件** 添加到 MakeCode 中。

* 打开 [https://makecode.microbit.org/](https://makecode.microbit.org/)
* 点击 **新项目**
* 点击齿轮图标菜单下的 **扩展**
* 搜索 **https://github.com/songxiao1018/micro-bit-eat-ben** 并导入

## 编辑此项目 ![构建状态标志](https://github.com/songxiao1018/micro-bit-eat-ben/workflows/MakeCode/badge.svg)

在 MakeCode 中编辑此仓库。

* 打开 [https://makecode.microbit.org/](https://makecode.microbit.org/)
* 点击 **导入**，然后点击 **导入 URL**
* 粘贴 **https://github.com/songxiao1018/micro-bit-eat-ben** 并点击导入

## 游戏玩法&基本运行逻辑

[在这里阅读详细代码解析](https://songxiao1018.github.io/micro-bit-eat-ben/daimajieshuo) 

* 游戏玩法

游戏目标：人物(较亮的点)吃掉豆子(较暗的点)
游戏操作：玩家可以通过前后左右倾斜micro：bit板子来控制人物的移动

* 游戏逻辑,详细见[这篇文章](http://www.xiaoxiaosky.top/2022/07/29/micro-bit-eat-ben-xiang-xi/)

```

> 程序初始化

 播放初始化音乐

 检测“A”键是否按下

> 游戏后台

 循环播放背景音乐

> 游戏主体

 将人物固定在中心

 生成“豆子”，注意与人物位置不同

> 开始游戏

 进行判断是否需要暂停游戏

 操作方法：同时按下“A”与“B”键。解除同理

 绘制人物与豆子的位置

 判断人物有没有走出棋盘

> 游戏结束

 输出得分

 是否重新开始游戏

> 操作方法：同时按下“A”与“B”键。解除同理

```

## 积木块预览

此图像显示主分支中最后一次提交的块代码。
此图像可能需要几分钟才能刷新。

![块的渲染视图](https://github.com/songxiao1018/micro-bit-eat-ben/raw/master/.github/makecode/blocks.png)

#### 元数据（用于搜索、渲染）

* for PXT/microbit
<script src="https://makecode.com/gh-pages-embed.js"></script><script>makeCodeRender("{{ site.makecode.home_url }}", "{{ site.github.owner_name }}/{{ site.github.repository_name }}");</script>
