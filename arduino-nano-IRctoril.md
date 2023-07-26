---
title: 基于Arduino的简易万能遥控器
date: 2023-02-14 00:08:04
categories: 开发
tags: 
  - arduino
  - CAD
---
# 基于Arduino的简易万能遥控器

## 1. 介绍

本项目是基于Arduino的万能遥控器，可以通过本遥控器控制电脑、电视、空调、机顶盒等设备。本项目的遥控器是基于Arduino Nano开发的，可以通过USB接口连接电脑，直接下载程序。同时，用户可以自己设定按键，实现自定义遥控器。

### 1.1 产品面向群体

本产品面向的群体是需要使用遥控器控制电脑、电视、空调、机顶盒等设备的用户。同时针对老龄化的用户本项目提出了简化按键数量，放大按键体积的理念，使得老年人也可以轻松使用本遥控器。

### 1.2 产品优势

  * 通过USB接口连接电脑，方便固件下载；
  * 通过Arduino IED开发，简单易用；
  * 针对特殊群体设计，简化按键数量，放大按键体积；

## 2. 产品外观

（本产品正处于开发阶段，未进行外壳设计）

![正面]()

![背面]()

## 2. 硬件设计

### 2.1 硬件boom表

| 原件名称 | 原件型号 | 代号 | 数量 | 备注 |
| --- | --- | --- | --- | --- |
| Arduino Nano | Arduino Nano | Arduino Nano | 1 |  |
| 电容 | 100nF | C1 | 2 | 10% 50V |
| 电容 | 220uF | C2 | 2 | 25V |
| 电阻 | 220 | R1 | 2 |  0.1% 125mW |
| AMS1117 | AMS1117-3.3 | AMS1117 | 1 |  |
| 红外发射二极管 | IRM-3638 | IRM-3638 | 1 |  |
| 红外接收二极管 | TSOP4838 | TSOP4838 | 1 |  |
| 按键 | 6x6x4.5mm | K1 | 8 |  |
| 自恢复保险丝 | 5.5A | F1 | 1 |  |


### 2.2 原理图

![Image: image]()

[pdf](files/keyboard-nano/keyboard-nano.pdf)

### 2.3 PCB

![Image: image]()

[pdf](files/keyboard-nano/keyboard-nano-pcb.pdf)

## 3. 软件

### 3.1 红外部分

#### 3.1.1 红外发射与接收原理

红外发射原理是通过红外发射二极管发射红外信号，通过红外接收二极管接收红外信号。红外发射二极管的引脚分别为GND、VCC，其中GND为地，VCC为电源同时为信号输入。红外接收二极管的引脚分别为GND、VCC、OUT，其中GND为地，VCC为电源，OUT为输出。红外发射二极管的VCC引脚连接到Arduino NANO的D3引脚。红外接收二极管的VCC引脚连接到Arduino NANO的VCC引脚，OUT引脚连接到Arduino的D2引脚。

#### 3.1.2 红外发射与接收代码

```c
#include <IRremote.h>

//红外 接收
int RECV_PIN = 2;
IRrecv irrecv(RECV_PIN);
decode_results results;

//红外 发射
IRsend irsend;

void setup(void) {
    //红外 初始化
    Serial.begin(9600);
    irrecv.enableIRIn(); // Start the receiver
}

void loop(void) {
    // 红外 发射
    irsend.sendNEC(0xFF18E7, 32);

    // 红外 接收
    if (irrecv.decode(&results)) {
        Serial.println(results.value, HEX);
        irrecv.resume(); // Receive the next value
    }
}
```

### 3.2 按键部分

#### 3.2.1 按键原理

按键原理是通过Arduino的数字输入引脚读取按键的状态，当按键按下时，引脚电平为低，当按键松开时，引脚电平为高。Arduino的数字输入引脚分别为D2、D3、D4、D5、D6、D7、D8、D9、D10、D11、D12、D13。本项目按键的引脚分别为D6、D7、D8、D9、D10、D11、D12、D13这8个。

#### 3.2.2 按键代码

```c
// 按键 初始化
int button6 = 0;
int button7 = 0;
int button8 = 0;
int button9 = 0;
int button10 = 0;
int button11 = 0;
int button12 = 0;
int button13 = 0;

void setup(void) {
    // 按键 初始化
    pinMode(6, INPUT);
    pinMode(7, INPUT);
    pinMode(8, INPUT);
    pinMode(9, INPUT);
    pinMode(10, INPUT);
    pinMode(11, INPUT);
    pinMode(12, INPUT);
    pinMode(13, OUTPUT);  
}

void loop(void) {
    // 按键 读取
    button6  = digitalRead(6);
    button7  = digitalRead(7);
    button8  = digitalRead(8);
    button9  = digitalRead(9);
    button10 = digitalRead(10);
    button11 = digitalRead(11);
    button12 = digitalRead(12);
  
    // 数据 发射
    if (button6  == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF18E7, 32);delay(100);}else {digitalWrite(13, LOW);}
    if (button7  == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFFA857, 32);delay(100);}else {digitalWrite(13, LOW);}
    if (button8  == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF30CF, 32);delay(100);}else {digitalWrite(13, LOW);}
    if (button9  == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFFD02F, 32);delay(100);}else {digitalWrite(13, LOW);}
    if (button10 == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF728D, 32);delay(100);}else {digitalWrite(13, LOW);}
    if (button11 == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF926D, 32);delay(100);}else {digitalWrite(13, LOW);}
    if (button12 == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF02FD, 32);delay(100);}else {digitalWrite(13, LOW);}
    if (button13 == HIGH) {irsend.sendNEC(0xFF926D, 32);delay(100);}
}
```

## 4. 效果

当按下按键时，红外发射二极管发射红外信号。
当红外接收二极管接收到红外信号，Arduino NANO通过串口打印红外信号的值。

## 5. 参考

## 6. 未来计划

* 加入蓝牙模块，实现蓝牙遥控。
* 加入WiFi模块，实现WiFi遥控。
* 加入LED灯珠，实现按键按下时亮灯。
* 加入OLED屏幕，实现屏幕显示遥控器的按键状态。
* 加入文件读取与写入，实现遥控器的按键状态保存与实时修改。

## 7. 附录

### 7.1 完整代码

```c
#include <IRremote.h>

// 按键 初始化
int button6 = 0;
int button7 = 0;
int button8 = 0;
int button9 = 0;
int button10 = 0;
int button11 = 0;
int button12 = 0;
int button13 = 0;

//红外 初始化
int RECV_PIN = 2;
IRrecv irrecv(RECV_PIN);
decode_results results;

IRsend irsend;

void setup(void) {
  // 按键 初始化
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  pinMode(10, INPUT);
  pinMode(11, INPUT);
  pinMode(12, INPUT);
  pinMode(13, OUTPUT);  

  //红外 初始化
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}

void loop(void) {
  button6  = digitalRead(6);
  button7  = digitalRead(7);
  button8  = digitalRead(8);
  button9  = digitalRead(9);
  button10 = digitalRead(10);
  button11 = digitalRead(11);
  button12 = digitalRead(12);
  
  if (button6  == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF18E7, 32);delay(100);}else {digitalWrite(13, LOW);}
  if (button7  == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFFA857, 32);delay(100);}else {digitalWrite(13, LOW);}
  if (button8  == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF30CF, 32);delay(100);}else {digitalWrite(13, LOW);}
  if (button9  == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFFD02F, 32);delay(100);}else {digitalWrite(13, LOW);}
  if (button10 == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF728D, 32);delay(100);}else {digitalWrite(13, LOW);}
  if (button11 == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF926D, 32);delay(100);}else {digitalWrite(13, LOW);}
  if (button12 == HIGH) {digitalWrite(13, HIGH);irsend.sendNEC(0xFF02FD, 32);delay(100);}else {digitalWrite(13, LOW);}
  // if (button13 == HIGH) {irsend.sendNEC(0xFF926D, 32);delay(100);}

  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);
    irrecv.resume();
  }
}
```

### 7.2 红外信号的读取

红外信号的值可以通过Arduino的串口打印出来，然后通过修改代码中的红外信号值，实现遥控器的按键状态的修改。
