#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import utility
import csv
import logging
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

class SearchWeiboMsg:
	def __init__(self, keyword):
		self.init(keyword);

	# 获取关键词微博前的初始化
	def init(self, keyword):
		self.flag = 0;		# 标记是否第一条记录,因为csv文件要在第一条记录前写标签
		self.keyword = keyword;

	# 对网页数据进行预处理
	def preprocess(self, content):
		bTag = 'node-type="feed_list">';
		eTag = '<div class="search_page clearfix"';
		bpos = content.find(bTag);
		temp = None;
		if(bpos != -1):
			bpos += len(bTag);
			epos = content.find(eTag, bpos);
			temp = '<div>' + content[bpos:epos] + '</div>';
			temp = temp.replace('\\/','/')
		self.content = temp;
		try:
			self.soup = BeautifulSoup(self.content);
		except Exception,e:
			logging.exception('页面预处理失败: ' + str(e));
			return False;
		return True;

	# 处理一个分页的微博数据,需要继续处理返回True,停止处理返回False
	def get_content(self, content):
		if( self.preprocess( content ) ):
			itemlist = self.soup.find_all('dl', attrs={'action-type':'feed_list_item'});
			if(itemlist != None):
				for item in itemlist:
					self.init_weibo();
					# 获取mid
					self.weibomsg['mid'] = item['mid'];
					# 获取uid,un,iu
					dt = item.dt;
					if(dt != None):
						a = dt.a;
						if(a != None):
							self.weibomsg['un'] = a['title'];
							uid = a['suda-data'];
							pos = uid.rfind(':');
							self.weibomsg['uid'] = uid[pos + 1:];
							img = a.img;
							if(img != None):
								self.weibomsg['iu'] = img['src'];
					
					# 获取微博内容主体 #
					dd = item.dd;
					# 获取mc
					self.weibomsg['mc'] = dd.em.get_text();
					# 获取转发消息
					retweet = dd.find('dl', attrs={'class':'comment W_textc W_linecolor W_bgcolor'});
					if(retweet != None): #转发内容
						pass;
					# 获取pu
					imglist = dd.find('ul', {'class':'piclist'});
					if(imglist != None):
						img = imglist.find('img', {'class':'bigcursor'});
						if(img != None):
							self.weibomsg['pu'] = img['src'];
					# 获取pt
					pt = dd.find('a', {'node-type':'feed_list_item_date'});
					if(pt != None):
						self.weibomsg['pt'] = pt['title'];
						self.weibomsg['page'] = pt['href'];
					# 获取srn
					srn = dd.find('a', {'rel':'nofollow'});
					if(srn != None):
						self.weibomsg['srn'] = srn.get_text();
					# 获取rc与cc
					rc = dd.find('a', {'action-type':'feed_list_forward'});
					if(rc != None):
						rc = rc.get_text();
						rc = utility.to_unicode(rc);
						temp = "";
						for i in rc:
							if(utility.is_number(i)):
								temp += i;
						if(temp != ''):
							self.weibomsg['rc'] = int(temp);
					cc = dd.find('a', {'action-type':'feed_list_comment'});
					if(cc != None):
						cc = cc.get_text();
						cc = utility.to_unicode(cc);
						temp = "";
						for i in cc:
							if(utility.is_number(i)):
								temp += i;
						if(temp != ''):
							self.weibomsg['cc'] = int(temp);
					#self.outputInfo();
					self.writeResult();
		return True;

	def init_weibo(self):
		self.weibomsg = {
			'uid':'',	#用户的id
			'un':'',	#用户用户名
			'iu':'',	#用户头像URL
			'mid':'',	#消息id
			'mc':'',	#消息内容
			'nc':'',	#消息中@的用户
			'run':'',	#转发的消息的用户名
			'rmc':'',	#转发的消息的内容
			'pu':'',	#消息中的图片
			'rrc':'',	#转发的消息的转发次数
			'rcc':'',	#转发的消息的评论次数
			'rpage':'',	#转发的消息的微博页面
			'rpt':'',	#转发的消息的发布时间
			'rc':'0',	#消息的转发次数
			'cc':'0',	#消息的评论次数
			'srn':'',	#消息来源
			'page':'',	#消息的微博页面
			'pt':''		#消息的发布时间
		};

	# 获取文件名
	def get_filename(self):
		filename = self.keyword.replace('/', '').replace(' ','_');
		filename = filename.lstrip('.').lstrip('-').lstrip('+');
		return filename;

	# 将一条微博记录写到csv文件
	def writeResult(self):
		#filename = './data/'+self.uid+'-'+self.weibomsg['un']+'.csv'
		filename = './data/' + self.get_filename() + '.csv'
		#utility.iprint('filename: '+filename)
		writer = csv.writer(file(filename,'a'))
		if self.flag == 0:
			writer.writerow(['uid','un','iu','mid','mc','run','rmc','pu','rrc','rcc','rpage','rpt','rc','cc','page','pt','srn'])
			self.flag = 1
		writer.writerow((self.weibomsg['uid'],self.weibomsg['un'],self.weibomsg['iu'],self.weibomsg['mid'],self.weibomsg['mc'],
			self.weibomsg['run'],self.weibomsg['rmc'],self.weibomsg['pu'],self.weibomsg['rrc'],self.weibomsg['rcc'],
			self.weibomsg['rpage'],self.weibomsg['rpt'],self.weibomsg['rc'],self.weibomsg['cc'],self.weibomsg['page'],
			self.weibomsg['pt'],self.weibomsg['srn']))
	
	# 输出微博信息到屏幕
	def outputInfo(self):
		print 'uid is :' + self.weibomsg['uid']
		print 'iu  is :' + self.weibomsg['iu']
		print 'un  is :' + self.weibomsg['un']
		print 'mid is :' + self.weibomsg['mid']
		print 'mc  is :' + self.weibomsg['mc']
		print 'nc  is :' + self.weibomsg['nc']
		print 'run is :' + self.weibomsg['run']
		print 'rmc is :' + self.weibomsg['rmc']
		print 'pu  is :' + self.weibomsg['pu']
		print 'rrc is :' + str(self.weibomsg['rrc'])
		print 'rcc is :' + str(self.weibomsg['rcc'])
		print 'rpt is :' + self.weibomsg['rpt']
		print 'rpage is :' + self.weibomsg['rpage'];
		print 'rc  is :' + str(self.weibomsg['rc'])
		print 'cc  is :' + str(self.weibomsg['cc'])
		print 'page is :' + self.weibomsg['page'];
		print 'pt  is :' + self.weibomsg['pt']
		print 'srn is :' + self.weibomsg['srn'];
		print '======================================'
		#time.sleep(1)