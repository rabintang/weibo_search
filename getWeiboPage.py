#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import utility
import logging
import SearchWeiboMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class getWeiboPage:	
	def __init__(self):
		self.charset = 'utf-8';
		self.wbmsg = None;

	def set_keyword(self, keyword):
		self.keyword = keyword

	def get_keyword(self):
		return self.keyword

	# 预处理,包括:构造传递参数等.成功返回True,否则返回False
	# sort: time => 按时间排序, hot => 按热门程度排序, 空为综合排序
	def preprocess(self, sort = 'time'):
		#构造url传递参数
		self.body = {
			'category':'4',
			'page':'1'
		};
		if( sort == 'time' or sort == 'hot'):
			self.body['xsort'] = sort;

		self.wbmsg = SearchWeiboMsg.SearchWeiboMsg(self.keyword);
		self.page_num = 1		# 微博总共有多少页
		self.flag = 0			# 标记是否已经获取页数
		return True;

	# 处理一个关键词的微博知识
	def get_msg(self, keyword, sort = 'time'):
		self.keyword = keyword;
		if( not self.preprocess( sort ) ):
			return;

		self.flag = 0;
		url = self.get_url();
		self.handle_one_page(url);
		for i in range(2, self.page_num+1):
			self.body['page'] = i			
			if( not self.handle_one_page(url) ):
				break;

	# 判断用户是否存在,存在返回True,否则返回False
	def keyword_exist(self, content):
		if(content.find('class="search_noresult">') != -1):
			return False;
		return True;

	# 获取微博页面的总页数,成功True,否则返回False
	def get_totallpage_num(self, content):
		try:
			if( self.keyword_exist(content) ):
				bTag = 'class="W_textc">';
				eTag = '<\/span>';
				pos1 = content.find(bTag);
				count = '';
				if( pos1 != -1 ):
					pos1 = pos1 + len(bTag);
					pos2 = content.find(eTag, pos1);
					if(pos2 != -1):
						slug = unicode(content[pos1:pos2], 'utf-8');
						for i in slug:
							if( utility.is_number(i) ):
								count += i;
						self.page_num = int(count);
				else:
					logging.info('%s 关键词总页数获取失败', self.get_keyword());
					return False;
			else:
				logging.info('%s 关键词不存在', self.get_keyword());
				return False;
		except Exception,e:
			logging.exception("%s 获取总页数失败: " + str(e), self.get_keyword());
			return False;

		page_num = self.page_num / 20;
		if(self.page_num % 20 != 0):
			page_num += 1;
		self.page_num = page_num;
		if(self.page_num > 50):
			self.page_num = 50;
		utility.iprint( self.get_keyword() + ':微博总共有 ' + str(self.page_num) + ' 页' )
		logging.info(self.get_keyword() + " 共有 %d 页微博", self.page_num);
		return True;

	# 获取第一分页微博,不用继续处理后续微博返回False
	def handle_one_page(self, url):
		content = self.download(url);
		if( content == None ):
			return True;
		if( self.flag == 0 ):
			if( not self.get_totallpage_num(content) ):
				return False;
			self.flag = 1;
		return self.wbmsg.get_content(content);
	
	# 获取用户微博页面的url
	def get_url(self):
		url = 'http://s.weibo.com/weibo/';
		return url

	# 下载网页,并进行解码,编码
	def download(self, url):
		try:
			url = url + urllib.quote(self.keyword)[:-3] + '&' + urllib.urlencode(self.body)
			print url;
			req = urllib2.Request(url)
			result = urllib2.urlopen(req)
			text = result.read()
		except Exception, e:
			logging.error('%s 网页下载失败: ' + str(e), url);
			return None;
		try:
			content = text.decode(self.charset, 'ignore');
			content = eval("u'''" + content + "'''").encode(self.charset);
		except Exception, e:
			logging.error('%s 网页解码失败: ' + str(e), url);
			return None;
		return content


if __name__ == '__main__':
	#getWeiboPage = getWeiboPage();
	pass;