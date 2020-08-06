#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020-03-23 17:52
# @Author  : fgyong 简书:_兜兜转转_  https://www.jianshu.com/u/6d1254c1d145
# @Site    : http://fgyong.cn 兜兜转转的技术博客
# @File    : dellogs.py
# @Software: PyCharm

import  os
import time  # 引入time模块
import re

def delFileName(name):
    if os.path.isfile(name):
        os.remove(name)
        print(name+'已删除')
    else:
        print('b不存在'+name)
def isDelFile(name):
    fArr = name.split('.')
    # laravel - 2020 - 03 - 23.log
    if len(fArr) == 2:
        if fArr[1] == 'log' and len(fArr[0]) == 18 and fArr[0][:7] == 'laravel':
            strLength = len(fArr[0])
            # if strLength >= 10:
            dateStr = fArr[0][strLength - 10:strLength]
            # print(dateStr)
            return isDateFile(dateStr)
    elif len(fArr) == 1 and len(name) == 10 :
        m = re.match("2[0-9]{3}-[0-9]{2}-[0-9]{2}",i)
        if m is not None:
            return isDateFile(i)
    return False

def isDateFile(dateStr):
    t = time.mktime(time.strptime(dateStr, '%Y-%m-%d'))
    nowTimes = time.time()
    timesdis = nowTimes - t
    # m = timesdis%60
    timesdis /= 60  # 转化分钟
    m = timesdis % 60
    h = timesdis / 60
    d = h / 24
    if timesdis >= timesDel:  # 删除一周 前的文件
        # print(i)
        return True

    print(str(int(d)) + "d" + str(int(h) % 24) + "h" + str(int(m)) + "m")
    return False
# filePath = ['/Users/Jerry/Desktop/未命名文件夹','/Users/Jerry/projectPHP/backCode']
filePath = ['/data']
delFiles = []
d = 60  * 24
timesDel = d * 1
if __name__ == '__main__':
    for i in delFiles:
        delFileName(i)
    for path in filePath:
        for root,dirsName,fileName in os.walk(path):
            for i in fileName:
                # print(os.path.join(root,i))

                if isDelFile(i):
                    print(os.path.join(root,i))
                # delFileName(i) # 删除文件

        # print(root)
