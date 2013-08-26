#!/usr/bin/python
#-*- coding:utf-8 -*-

#import MySQLdb
import feedparser
import time
import codecs
from hashlib import md5
import sys
import re


#mysql_connection = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '19911230', db = 'RSS4Kindle', charset = "utf8")
#cur = mysql_connection.cursor()

def generateHTML(item):
	#tmp_html = codecs.open(item['title'].replace('/', '\\') + '.html', 'w', 'utf-8')
	tmp_html = codecs.open(item['title'] + '.html', 'w', 'utf-8')
	tmp_html.write("<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"zh-CN\">\n")
	tmp_html.write("<head>\n")
	tmp_html.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n")
	tmp_html.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"css/main.css\"/>\n")
	tmp_html.write("<title>" + item['title'] + "</title>\n")
	tmp_html.write("</head>\n")
	tmp_html.write("<body>\n")
	tmp_html.write(item['description'])
	contents = item.get('content')
	if contents != None:
		for content in contents:
			tmp_html.write(content['value'])
			download_url(content['value'])

	tmp_html.write("</body>\n")
	tmp_html.write("</html>\n")
	tmp_html.close()

def suffix(url):
	return url.split('.')[-1]

def download_url(lines):
	print lines
	md5sum = md5()
	index = 0
	while True:
		start = lines.find('src="', index) + 5
		end = lines.find('"', start)
		if end == -1:
			break
		index = end + 1
		url = lines[start : end]
		print url
		md5sum.update(url)
		path = str(md5sum.hexdigest()) + "." + suffix(url)
		urllib.urlretrieve(url, path)

def fetch_url(url):
	feed = feedparser.parse(url)
	items = feed['items']
	print feed['channel']['title']
	item_list = { 'title' : feed['channel']['title'], 'items' : [] }
	for item in items:
		#cur.execute('select * from RSSItems where ItemLink = "%s"', item['link'])

		#if cur.rowcount == 0:
		#	args = (feed['url'], item['title'], item['link'], time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']))
		#	cur.execute('insert into RSSItems (RSSFeedURL, ItemTitle, ItemLink, ItemPubDate) values \
		#		("%s", "%s", "%s", %s)', args)
		#else:
		#	generateHTML(item)

		contents = item.get('content')
		if contents != None:
			for content in contents:
				download_url(content['value'])

		item_list['items'].append(item['title'].replace('/', '\\') + '.html')
		pattern = re.compile(r'src=')
		contents = item.get('content')
		for content in contents:
			match = pattern.match(content['value'])
			if match:
				print match.group()
	#print item_list
	return item_list

def get_RSSTags():
	cur.execute('select distinct RSSTag from RSSFeeds');
	tags = cur.fetchall()
	for tag in tags:
		args = (tag)
		cur.execute('select RSSFeedURL from RSSFeeds where RSSTag = %s', args)
		feed_urls = cur.fetchall()
		for feed_url in feed_urls:
			print feed_url[0]
			fetch_url(feed_url[0])

def generate_manifest(href_list):
	md5sum = md5()
	result = ""
	idref_list = []
	for href in href_list:
		md5sum.update(href.get('href'))
		result += '<item href=\"' + href.get('href') + '\" media-type=' + href.get('filetype', "\"application/xhtml+xml\"") + ' id=\"' + md5sum.hexdigest() + '\"/>\n'
		idref_list.append(md5sum.hexdigest())
	print generate_spine(idref_list)
	return result

def generate_spine(idref_list):
	result = ""
	for idref in idref_list:
		result += '<itemref idref=\"' + idref + '\"/>\n'
	return result

def generate_guide(reference_list):
	m = md5()
	m.update("123")
	print m.hexdigest()
	pass

def generate_opf(item_list):
	pass

def generate_ncx():
	pass

def generate_book_index():
	pass

href_list = [{'href' :"1.html", 'filetype' : "\"application/xhtml+xml\""}, {'href' : "2.html", 'filetype' : "\"application/xhtml+xml\""}, {'href' : "3.html", 'filetype' : "\"application/xhtml+xml\""}]
print generate_manifest(href_list)
fetch_url('http://coolshell.cn/feed')

#cur.close()
#mysql_connection.commit()
#mysql_connection.close()