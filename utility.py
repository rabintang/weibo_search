# -*- coding: utf-8 -*-

import time
from datetime import datetime
from datetime import timedelta
import os
import csv
import platform
import sys
import GlobalVal as GV

reload(sys)
sys.setdefaultencoding('utf-8')

#获取系统当前时间
def now():
    return time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))

#格式化时间
def time_format(origin):
    year = time.strftime('%Y',time.localtime(time.time()));
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()));
    now = datetime.now();

    if( origin.find('今天') != -1 ):
        format = date + origin[2:];
    elif( origin.find('分钟前') != -1 ):
        minus = int(origin[0:-3]) * -1;
        minus = timedelta(minutes=minus);
        format = datetime.now() + minus;
        format = format.strftime('%Y-%m-%d %H:%M');
    elif( origin.find('月') != -1 ):
        end = origin.find('月');
        month = origin[0:end];
        begin = end + 3;
        end = origin.find('日');
        day = origin[begin:end];
        format = year + '-' + month + '-' + day + origin[end+3:];
    else:
        format = origin;
    return format;

# 是否超过时间间隔
def time_exceed(time, interval = -15):
    date_time = datetime.strptime(time,'%Y-%m-%d %H:%M');
    earlist_day = datetime.now() + timedelta(days=interval);
    if( earlist_day > date_time ):
        return True;
    return False;

#字符串是否只含空白
def isEmpty(text):
    text = text.replace(' ','').replace('\n','').replace('\t','')
    if len(text) == 0:
        return True
    return False

#清除数据中的空白及斜杆
def clearSpace(text):
    text = text.replace('\r\n','').replace('\n','').replace('\t','').replace('\\/','/')
    text = text.strip();
    return text

#创建文件夹路径
def createDirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except:
        print 'directory',path,'created error'
        return False
    return True

#创建文件
def createFile(path,name):
    try:
        if path[len(path)-1] != '/':
            path = path + '/'
        filePath = path + name
        if not os.path.exists(filePath):            
            if not createDirs(path):
                return None
        f = open(filePath,'w')
        return f
    except:
        print 'file',filePath,'created error'
        return None

# 写入文件
def write_file(content, filepath):
    pos = filepath.rfind('/');
    path = './';
    filename = path;
    if(pos != -1):
        path = filepath[:pos];
        filename = filepath[pos+1:];
    writer = createFile(path,filename);
    writer.write(content);
    writer.close();

#以操作系统默认编码打印字符串,参数str的编码为utf-8
def iprint(str):
	sysstr = platform.system()
	if(sysstr =="Windows"):
		print str.decode('utf-8').encode('gbk')
	else:
		print str

# 将字符串编码为unicode
def to_unicode(origin, decode='utf-8'):
    try:
        if(isinstance(origin, unicode)):
            return origin;
        else:
            return unicode(origin, decode);
    except:
        return None;

# 是否数字
def is_number(i):
    return 0x0030<=ord(i)<=0x0039;

# 是否英文字母
def is_en_char(i):
    return ( 0x0041<=ord(i)<=0x005a ) or ( 0x0061<=ord(i)<=0x007a );

# 是否中文字符
def is_cn_char(i):
    return 0x4e00<=ord(i)<=0x9fa5;
