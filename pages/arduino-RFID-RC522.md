---
title: arduino与RFID-RC522模块实现IC卡读取与写入（待整理）
date: 2023-01-06 09:20:51
categories:
tags:
---
https://blog.csdn.net/weixin_43031092/article/details/108651982

简介
单片机：Arduino Uno
额外库：MFRC522（可直接在库管理器下载）

S50 IC卡 采用NXP MF1 IC S50制作的非接触智能卡，通常简称S50卡或Mifare 1K，符合ISO14443A标准；存储容量：8Kbit，16个分区，每分区两组密码。

枯叶笑与东方大叔的IC卡小结
分类 IC - ID
市场上常用的卡片就两种，IC卡和ID卡，这两者的区别就是IC卡有存储芯片（如M1,UID,CUID,FUID,UFUID），而 ID卡只是一个卡号（ 全称为身份识别卡，是一种不可写入的感应卡，含固定的编号.卡号在封卡前写入后不可再更改）。CPU卡因为价格太高，没有推广起来

IC卡的芯片，目前市场上常用的有两种，一种是价格较高的飞利浦原装芯片，一种是上海复旦芯片；原装飞利浦芯片IC卡，市场拿货价不超过3元，例如公交卡，国产芯片IC卡，价格几毛钱，常用于电梯、停车场、食堂就餐、水卡

IC卡和ID卡都可以用于一卡通系统，各有优缺点：

ID卡，因为只是ID号，没有内置存储芯片，因此，当ID卡用于一卡通系统时，必须要电脑开着，因为，你消费扣款或充值，都是从电脑数据库里加加减减，这类似于磁条性质的银行卡，卡片本身没有钱，你取钱存钱，其实都是在银行数据库里加减

优点：因为是从电脑数据库里直接加减，因此，充值或取款，卡片无需到场，刷卡数据实时传输到电脑
缺点：电脑坏了或通讯有问题，整套系统都瘫痪（脱机消费模式也行，这里不具体讲）
IC卡，常用的公交卡、地铁卡都是IC卡，内置芯片，0-15 共16个扇区，可以写入数据

优点：因为钱是直接存储在卡里面，因此，消费时，无需联网，跟电脑无关，直接从卡里面扣钱
缺点：充值时，卡片必须到场 （省事的方法，补贴机之类），刷卡数据暂时储存在刷卡机里，待电脑开机后，采集消费数据到电脑
IC细分类
M1 卡
普通IC卡，0扇区不可以修改，其他扇区可反复擦写，我们使用的电梯卡、门禁卡等智能卡发卡商所使用的都是 M1 卡，可以理解为物业发的原卡。

UID 卡
普通复制卡，可以重复擦写所有扇区，主要应用在IC卡复制上，遇到带有防火墙的读卡器就会失效。

CUID 卡
可擦写防屏蔽卡，可以重复擦写所有扇区，UID卡复制无效的情况下使用，可以绕过防火墙。
（防屏蔽就是防止某些设备里面有检测机制能够检查出卡片是否为复制卡，cuid卡比较常用，需要注意第二次使用需要格式化，还有说明一下 0扇区就是机器与卡片的桥梁用来存放对应信息。）

FUID 卡
不可擦写防屏蔽卡，此卡的特点0扇区只能写入一次，写入一次变成 M1 卡，CUID 复制没用的情况下使用，可以绕过防火墙。

UFUID 卡
高级复制卡，我们就理解为是 UID 和 FUID 的合成卡，需要封卡操作，不封卡就是 UID 卡，封卡后就变为 M1 卡。

工具
ACR122
使用最多的读卡器，很流行，大抵是因为网络上流传了非常强大的GUI改卡读卡复制卡软件吧。

Proxmark3
国外的开源硬件，由FPGA驱动。性能十分强大，集嗅探、读取、克隆于一体，IC卡和ID卡通杀。

PN532
由NXP出品，是一款高度集成的载波的13.56MHz传输模块，基于80C51内核有40KROM、1KRAM。某宝价格为几十元，非常便宜。只能用来读取IC卡，不能读取ID卡和CPU卡。

入门
引脚接线
常用接线也在示例程序中写明，这里我使用的是Arduino Uno，所以接线参考前两列即可。

 * Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS      SDA(SS)      10            53        D10        10               10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 */
1
2
3
4
5
6
7
8
9
10
11
12
即（左侧为RFID-RC522引脚，右侧为Uno引脚）
RST <----------> 9
SDA(SS) <----------> 10
MOSI <----------> 11
MISO <----------> 12
SCK <----------> 13
3.3V <----------> 3.3V
GND <----------> GND


读取 UNID <-> 卡号 <-> ID号
这里使用的是MFRC522库中的示例-ReadUNID，读取卡号。
据说每一张卡的ID都不一样-,-读取卡号就能判断身份，不过最好是先尝试写入数据（尝试修改卡号），能修改的卡说明是复制卡，这就需要认真对待这样卡的安全性了。

Sketch

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
 
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

MFRC522::MIFARE_Key key; 

// Init array that will store new NUID 
byte nuidPICC[4];

void setup() { 
  Serial.begin(9600);
  SPI.begin(); // Init SPI bus
  Serial.println(F("Start--------------------"));
  rfid.PCD_Init(); // Init MFRC522 

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  Serial.println(F("This code scan the MIFARE Classsic NUID."));
  Serial.print(F("Using the following key:"));
  printHex(key.keyByte, MFRC522::MF_KEY_SIZE);
}
 
void loop() {

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;

  Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  Serial.println(rfid.PICC_GetTypeName(piccType));

  // Check is the PICC of Classic MIFARE type
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&  
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }

  if (rfid.uid.uidByte[0] != nuidPICC[0] || 
    rfid.uid.uidByte[1] != nuidPICC[1] || 
    rfid.uid.uidByte[2] != nuidPICC[2] || 
    rfid.uid.uidByte[3] != nuidPICC[3] ) {
    Serial.println(F("A new card has been detected."));

    // Store NUID into nuidPICC array
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
    }
   
    Serial.println(F("The NUID tag is:"));
    Serial.print(F("In hex: "));
    printHex(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();
    Serial.print(F("In dec: "));
    printDec(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();
  }
  else Serial.println(F("Card read previously."));

  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
}


/**
 * Helper routine to dump a byte array as hex values to Serial. 
 */
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

/**
 * Helper routine to dump a byte array as dec values to Serial.
 */
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
结果
打开Arduino的串口监视器，下载好程序，把IC卡刷到RFID-RC522模块上有标记线圈的位置，就能在串口监视器中看到其编号（饭卡、银行卡刷不出来。。。。。）


写入&&读取个人信息：名+姓氏
接线请往上爬，一模一样。

Sketch-写入
rfid_write_personal_data.ino

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9           // Configurable, see typical pin layout above
#define SS_PIN          10          // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance

void setup() {
  Serial.begin(9600);        // Initialize serial communications with the PC
  SPI.begin();               // Init SPI bus
  mfrc522.PCD_Init();        // Init MFRC522 card
  Serial.println(F("Write personal data on a MIFARE PICC "));
}

void loop() {

  // Prepare key - all keys are set to FFFFFFFFFFFFh at chip delivery from the factory.
  MFRC522::MIFARE_Key key;
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  Serial.print(F("Card UID:"));    //Dump UID
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.print(F(" PICC type: "));   // Dump PICC type
  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.println(mfrc522.PICC_GetTypeName(piccType));

  byte buffer[34];
  byte block;
  MFRC522::StatusCode status;
  byte len;

  Serial.setTimeout(20000L) ;     // wait until 20 seconds for input from serial
  // Ask personal data: Family name
  Serial.println(F("Type Family name, ending with #"));
  len = Serial.readBytesUntil('#', (char *) buffer, 30) ; // read family name from serial
  for (byte i = len; i < 30; i++) buffer[i] = ' ';     // pad with spaces

  block = 1;
  //Serial.println(F("Authenticating using key A..."));
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }
  else Serial.println(F("PCD_Authenticate() success: "));

  // Write block
  status = mfrc522.MIFARE_Write(block, buffer, 16);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Write() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }
  else Serial.println(F("MIFARE_Write() success: "));

  block = 2;
  //Serial.println(F("Authenticating using key A..."));
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  // Write block
  status = mfrc522.MIFARE_Write(block, &buffer[16], 16);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Write() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }
  else Serial.println(F("MIFARE_Write() success: "));

  // Ask personal data: First name
  Serial.println(F("Type First name, ending with #"));
  len = Serial.readBytesUntil('#', (char *) buffer, 20) ; // read first name from serial
  for (byte i = len; i < 20; i++) buffer[i] = ' ';     // pad with spaces

  block = 4;
  //Serial.println(F("Authenticating using key A..."));
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  // Write block
  status = mfrc522.MIFARE_Write(block, buffer, 16);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Write() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }
  else Serial.println(F("MIFARE_Write() success: "));

  block = 5;
  //Serial.println(F("Authenticating using key A..."));
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  // Write block
  status = mfrc522.MIFARE_Write(block, &buffer[16], 16);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Write() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }
  else Serial.println(F("MIFARE_Write() success: "));


  Serial.println(" ");
  mfrc522.PICC_HaltA(); // Halt PICC
  mfrc522.PCD_StopCrypto1();  // Stop encryption on PCD

}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
Result

例如我第一次输入 Smith#
第二次输入 Rick#

Sketch-读取
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9           // Configurable, see typical pin layout above
#define SS_PIN          10          // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance

//*****************************************************************************************//
void setup() {
  Serial.begin(9600);                                           // Initialize serial communications with the PC
  SPI.begin();                                                  // Init SPI bus
  mfrc522.PCD_Init();                                              // Init MFRC522 card
  Serial.println(F("Read personal data on a MIFARE PICC:"));    //shows in serial that it is ready to read
}

//*****************************************************************************************//
void loop() {

  // Prepare key - all keys are set to FFFFFFFFFFFFh at chip delivery from the factory.
  MFRC522::MIFARE_Key key;
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;

  //some variables we need
  byte block;
  byte len;
  MFRC522::StatusCode status;

  //-------------------------------------------

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  Serial.println(F("**Card Detected:**"));

  //-------------------------------------------

  mfrc522.PICC_DumpDetailsToSerial(&(mfrc522.uid)); //dump some details about the card

  //mfrc522.PICC_DumpToSerial(&(mfrc522.uid));      //uncomment this to see all blocks in hex

  //-------------------------------------------

  Serial.print(F("Name: "));

  byte buffer1[18];

  block = 4;
  len = 18;

  //------------------------------------------- GET FIRST NAME
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 4, &key, &(mfrc522.uid)); //line 834 of MFRC522.cpp file
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Authentication failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  status = mfrc522.MIFARE_Read(block, buffer1, &len);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Reading failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  //PRINT FIRST NAME
  for (uint8_t i = 0; i < 16; i++)
  {
    if (buffer1[i] != 32)
    {
      Serial.write(buffer1[i]);
    }
  }
  Serial.print(" ");

  //---------------------------------------- GET LAST NAME

  byte buffer2[18];
  block = 1;

  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 1, &key, &(mfrc522.uid)); //line 834
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Authentication failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  status = mfrc522.MIFARE_Read(block, buffer2, &len);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Reading failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return;
  }

  //PRINT LAST NAME
  for (uint8_t i = 0; i < 16; i++) {
    Serial.write(buffer2[i] );
  }


  //----------------------------------------

  Serial.println(F("\n**End Reading**\n"));

  delay(1000); //change value if you want to read cards faster

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
Result

正如上面所输入的一样-.-

读取扇区数据
以S50为例，读取其中16个扇区的全部数据,烧录程序后刷一下就能在串口监视器看到所有扇区对应的数据了

Sketch
Dumpinfo.info

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9          // Configurable, see typical pin layout above
#define SS_PIN          10         // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

void setup() {
	Serial.begin(9600);		// Initialize serial communications with the PC
	while (!Serial);		// Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();		// Init MFRC522
	delay(4);				// Optional delay. Some board do need more time after init to be ready, see Readme
	mfrc522.PCD_DumpVersionToSerial();	// Show details of PCD - MFRC522 Card Reader details
	Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
}

void loop() {
	// Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
	if ( ! mfrc522.PICC_IsNewCardPresent()) {
		return;
	}

	// Select one of the cards
	if ( ! mfrc522.PICC_ReadCardSerial()) {
		return;
	}

	// Dump debug info about the card; PICC_HaltA() is automatically called
	mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
Result


References
Arduino教程 RFID-RC522读IC卡门禁原理
Introduction to NFC
产品资料 提取码: qi6v
M1 : S50和S70
IC卡小结
————————————————
版权声明：本文为CSDN博主「Kearney form An idea」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_43031092/article/details/108651982



https://blog.csdn.net/leytton/article/details/73480974


【文章特色：1、提出IC卡破解原理和简单有效的防御方法2、网上其他文章对于硬件如何接线说得模糊不清】
1、序言
先说下简单门禁系统的原理：

(1)IC卡激活：门禁卡管理员将卡片放到读卡器、这时软件读取到IC卡的UID序列号信息(相当于身份证号码)，将这个UID录入数据库激活IC卡。

(2)刷卡：刷卡时读卡器读取到UID，查询数据库，如果数据库中存在这个UID则表示有效用户,继而控制继电器断电，此时电磁锁开门。


不亦买的RC522模块采用SPI通信、据说也有串口通信的不过成本较高。大家可以看看这个模块的主要配件：卡和读卡器。

2、加载RC522库文件
 Arduino本身有个操作RC5200的库，如下图所示，打开Arduino开发工具中管理库



搜索"RC522"，选择"MFRC522"安装即可

点击"More info"可以跳转到github地址https://github.com/miguelbalboa/rfid ，下文会有提及。


安装完毕后，可以看到关于MFRC522的库示例，有读取UID、获取区块信息、修改UID、卡片信息复制等

注：一般而言IC卡是不能修改0扇区0区块的UID和厂商信息数据，这些是生产时就确定下来的的(关于IC卡的存储结构有空再发文介绍，小伙伴们可以去网上查阅这方面资料也挺多的)，能够全扇区修改的俗称UID卡才支持修改UID，一些不负责的门禁系统厂家仅根据UID来判断用户身份是不可靠的，一个简单的方法是在读之前先写UID操作，如果可写那么这张卡就是UID卡即复制卡，判断无效，系统也可记录是哪张IC卡被复制了用于追溯非法行为，仅供交流与学习，请勿用于非法用途哦



3、模块引脚接线
此处是网络上大部分相关文章没有提及的，只告诉了如何接线，却不告诉我们为什么这样接，甚至连Arduino版本都不说清楚。

我们打开ReadNUID的示例里面有各种版本Arduino与RC522的引脚连接图，我们按照这个接线即可。在上文提及的github项目主页也有介绍。

RC522一共8个引脚，如图所示：


3.3V供电、GND接地不用多说，IRQ是中断才用到的此处没有用到可以不接，其余5个引脚接法如下表所示：

 /* Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS      SDA(SS)      10            53        D10        10               10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 */

4、程序代码
此处测试的Arduino型号是Arduino Nano V3.0，其他型号请结合上表修改引脚号。

示例代码读取UID，并将其分别以十进制和十六进制输出到串口，简化版如下：

#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN 10
#define RST_PIN 9
 
MFRC522 rfid(SS_PIN, RST_PIN); //实例化类
 
// 初始化数组用于存储读取到的NUID 
byte nuidPICC[4];
 
void setup() { 
  Serial.begin(9600);
  SPI.begin(); // 初始化SPI总线
  rfid.PCD_Init(); // 初始化 MFRC522 
}
 
void loop() {
 
  // 找卡
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
 
  // 验证NUID是否可读
  if ( ! rfid.PICC_ReadCardSerial())
    return;
 
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
 
  // 检查是否MIFARE卡类型
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&  
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println("不支持读取此卡类型");
    return;
  }
  
  // 将NUID保存到nuidPICC数组
  for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = rfid.uid.uidByte[i];
  }   
  Serial.print("十六进制UID：");
  printHex(rfid.uid.uidByte, rfid.uid.size);
  Serial.println();
  
  Serial.print("十进制UID：");
  printDec(rfid.uid.uidByte, rfid.uid.size);
  Serial.println();
  
  // 使放置在读卡区的IC卡进入休眠状态，不再重复读卡
  rfid.PICC_HaltA();
 
  // 停止读卡模块编码
  rfid.PCD_StopCrypto1();
}
 
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : "");
    Serial.print(buffer[i], HEX);
  }
}
 
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : "");
    Serial.print(buffer[i], DEC);
  }
}

5、运行结果
依次将卡A、卡B、卡A放到RC522读卡区，串口打印信息如下


感谢梦鸽推上首页分享给更多的人看到^_^
【转载请注明出处: http://blog.csdn.net/leytton/article/details/73480974】
 PS：如果本文对您有帮助，请点个赞让我知道哦~
————————————————
版权声明：本文为CSDN博主「李乾文」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/leytton/article/details/73480974