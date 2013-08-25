#!/usr/bin/python
#-*- coding:utf-8 -*-

import MySQLdb
import feedparser
import time
import codecs


mysql_connection = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '19911230', db = 'RSS4Kindle', charset = "utf8")
cur = mysql_connection.cursor()

def generateHTML(item):
	tmp_html = codecs.open(item['title'].replace('/', '\\') + '.html', 'w', 'utf-8')
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

	tmp_html.write("</body>\n")
	tmp_html.write("</html>\n")
	tmp_html.close()

def fetch_url(url):
	feed = feedparser.parse(url)
	items = feed['items']
	for item in items:
		cur.execute('select * from RSSItems where ItemLink = "%s"', item['link'])

		if cur.rowcount == 0:
			args = (feed['url'], item['title'], item['link'], time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']))
			cur.execute('insert into RSSItems (RSSFeedURL, ItemTitle, ItemLink, ItemPubDate) values \
				("%s", "%s", "%s", %s)', args)
		else:
			generateHTML(item)

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
	pass

def generate_spine(idref_list):
	pass

def generate_guide(reference_list):
	pass

def generate_opf(item_list):
	pass

def generate_ncx():
	pass

def generate_book_index():
	pass

cur.close()
mysql_connection.commit()
mysql_connection.close()