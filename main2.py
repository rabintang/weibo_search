#!/usr/bin/python
# -*- coding: utf-8 -*-

import weiboLogin
import urllib
import urllib2
import time
import os
import getWeiboPage
import threading
import logging
import utility
import GlobalVal as GV
mylock = threading.RLock()
   
class worker(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self);
		self.t_name = name;
		self.thread_stop = False;

	def run(self):
		global task_list;

		WBcontent = getWeiboPage.getWeiboPage();
		while not GV.task_list.empty() and not self.thread_stop:
			keyword = GV.task_list.get();
			utility.iprint( "还剩下 %d 个任务" % GV.task_list.qsize() );
			if keyword:
				WBcontent.set_keyword( keyword );
				utility.iprint( 'Thread %s handle id:%s'%( self.t_name, WBcontent.get_keyword() ) );
				try:
					WBcontent.get_msg(WBcontent.get_keyword());
				except Exception, e:					
					logging.exception( "%s 用户信息解析出错:" + str(e), WBcontent.get_keyword() );
					continue;

	def stop(self):
		self.thread_stop = True;

def test():
	WBcontent = getWeiboPage.getWeiboPage();
	while not GV.task_list.empty():
		keyword = GV.task_list.get();
		utility.iprint( "还剩下 %d 个任务" % GV.task_list.qsize() );
		if keyword:
			WBcontent.set_keyword(keyword);
			utility.iprint( 'handle id:%s'%WBcontent.get_keyword() );
			try:
				WBcontent.get_msg(WBcontent.get_keyword());
			except Exception, e:
				logging.exception(keyword + "用户信息解析出错: " + str(e));
				continue;

def controller():
	num = input('input threads number:')
	for i in range(1, num+1):
		worker('T'+str(i)).start()

	while True:
		time.sleep(60);
		count = threading.activeCount();
		utility.iprint( '还有 %d 个活动线程'%count );
		if(count < num and not GV.task_list.empty()):
			for j in range(count-1, num):
				 worker('T' + str(j)).start();
		elif(GV.task_list.empty() and count <= 1):
			break;

def init():
	# 配置日志
	# '[%(asctime)s]-%(levelname)s : %(message)s'
	logging.basicConfig(filename='weibo.log',filemode='a',format='[%(asctime)s] - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s',level=logging.DEBUG)

	# 进行模拟登录
	filename = './config/account'#保存微博账号的用户名和密码，第一行为用户名，第二行为密码
	WBLogin = weiboLogin.weiboLogin()
	if WBLogin.login(filename)==1:
		print 'Login success!'
	else:
		print 'Login error!'
		exit()

	# 生成任务
	reader = open('task','r');
	for line in reader:
		line = line.encode('utf-8');
		GV.task_list.put(line);

	# 开始执行任务
	controller();
	#test();

if __name__== '__main__':
    init();
    #test_exist_key();