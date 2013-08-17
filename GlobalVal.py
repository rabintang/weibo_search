#!/usr/bin/python
#-*- coding: utf-8 -*-

import Queue

# 此文件用于定义一些全局变量

# 数据库配置信息 #
server = '219.223.251.32';
user = 'root';
pwd = '';
database = 'weiboapp';

dict_klg = {};	# 词条数据

task_list = Queue.Queue();	# 待完成的任务