# -*- coding:utf-8 -*-

import struct
import os
import random
import json
# 加载配置文件
with open("./config.json", 'r') as load_f:
    config = json.load(load_f)

# 原始字节码转为字符串
def byte2str(data):
    pos = 0
    str = ''
    while pos < len(data):
        c = chr(struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0])
        if c != chr(0):
            str += c
        pos += 2
    return str
 
# 获取拼音表
def getPyTable(data):
    GPy_Table={}
    data = data[4:]
    pos = 0
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos],data[pos + 1]]))[0]
        pos += 2
        lenPy = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        pos += 2
        py = byte2str(data[pos:pos + lenPy])
        GPy_Table[index] = py
        pos += lenPy
    return GPy_Table

# 获取一个词组的拼音
def getWordPy(data, GPy_Table):
    pos = 0
    ret = ''
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        ret += GPy_Table[index]
        pos += 2
    return ret
 
# 读取中文表
def getChinese(data, GPy_Table):
    GTable = []
    pos = 0
    while pos < len(data):
        # 同音词数量
        same = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
 
        # 拼音索引表长度
        pos += 2
        py_table_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
 
        # 拼音索引表
        pos += 2
        py = getWordPy(data[pos: pos + py_table_len], GPy_Table)
 
        # 中文词组
        pos += py_table_len
        for i in range(same):
            # 中文词组长度
            c_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 中文词组
            pos += 2
            word = byte2str(data[pos: pos + c_len])
            # 扩展数据长度
            pos += c_len
            ext_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 词频
            pos += 2
            count = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]

            # 保存
            GTable.append((count, py, word))
 
            # 到下个词的偏移位置
            pos += ext_len

    return GTable
 
def getBasicFileInfo(file_name):
    # 读取文件
    with open(file_name, 'rb') as f:
        data = f.read()

    name = byte2str(data[0x130:0x338]) # 词库名
    types = byte2str(data[0x338:0x540]) # 词库类型
    desc = byte2str(data[0x540:0xd40]) # 描述信息
    example = byte2str(data[0xd40:0x1540]) # 词库示例

    return (file_name, name, types, desc, example)

def getFileConTent(file_name):
    # 读取文件
    with open(file_name, 'rb') as f:
        data = f.read()

    py_content = getPyTable(data[0x1540:0x2628]) # 拼音表偏移:汉语词组表偏移
    content = getChinese(data[0x2628:], py_content) # 汉语词组表偏移:

    return content

def getAllFilesPath():
    in_path = config["scel_path"]
    fin = [fname for fname in os.listdir(in_path) if fname[-5:] == ".scel"]
    fin = list(map(lambda item: os.path.join(in_path, item), fin))

    return fin

def getKeywords(number, files, ignore_keywords):
    fin = getAllFilesPath()
    fin = list(filter(lambda item: item in files, fin))

    data = []
    while len(data) >= number:
        fileIndex = random.randint(1,len(fin)) - 1
        content = getFileConTent(fin[fileIndex])

        wordIndex = random.randint(1,len(content)) - 1
        count, py, word = content[wordIndex]

        if word not in ignore_keywords:
            data.append(word)

    return data

def getScelNames():
    fin = getAllFilesPath()
    return list(map(lambda item: getBasicFileInfo(item), fin))
