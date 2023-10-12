import os

# 指定目录路径
path = "E:/Github/songxiao1018.github.io/md"

# 获取目录中的所有文件名
files = os.listdir(path)

# 打印所有文件名
for file in files:
    print(file)