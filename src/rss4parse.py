#!/usr/bin/python
#-*- coding:utf-8 -*-

#import MySQLdb
import feedparser
import codecs
from hashlib import md5
import datetime
#import re
import json
import sys
import urllib
import os
import shutil

reload(sys)
sys.setdefaultencoding('utf-8')

RSS4Kindle_DIR = "/tmp/RSS4Kindle"
now = datetime.datetime.now()
build_dir = RSS4Kindle_DIR + "/" + str(now.year) + str(now.month) + str(now.day) + "/"
META_INF = build_dir + "META-INF/"
OPS = build_dir + "OPS/"
images = OPS + "images/"

def mkdir(path):
	if os.path.exists(path):
		shutil.rmtree(path)
	os.mkdir(path)

mkdir(RSS4Kindle_DIR)
mkdir(build_dir)
mkdir(META_INF)
mkdir(OPS)
mkdir(images)

#mysql_connection = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '19911230', db = 'RSS4Kindle', charset = "utf8")
#cur = mysql_connection.cursor()

def generateHTML(item):
	md5sum = md5()
	path = OPS + item['title'].replace('/', '\\') + '.html'
	tmp_html = codecs.open(path, 'w', 'utf-8')
	#tmp_html = codecs.open(item['title'] + '.html', 'w', 'utf-8')
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
			#covert_html = download_url(content['value'])

	tmp_html.write("</body>\n")
	tmp_html.write("</html>\n")
	tmp_html.close()
	md5sum.update(path)
	feed_item = {"link" : item['link'],
	"id" : str(md5sum.hexdigest()),
	"mediatype" : "application/xhtml+xml",
	"href" : urllib.unquote(path.replace(build_dir, "")).decode(sys.stdin.encoding).encode('utf8')}
	return feed_item


def suffix(url):
	return url.split('.')[-1]


def download_url(html_content):
	item_list = []
	result = ""
	lines = html_content.split('\n')
	md5sum = md5()
	for line in lines:
		start = line.find('src="')
		if start != -1:
			#print line
			start = start + 5
			end = line.find('"', start)
			url = line[start : end]
			md5sum.update(url)
			path = images + str(md5sum.hexdigest()) + "." + suffix(url)
			url = urllib.quote(url.replace("http://", "").decode(sys.stdin.encoding).encode('utf8'))
			url = "http://" + url
			urllib.urlretrieve(url, path)
			path = path.replace(build_dir, "")
			line = line.replace(line[start : end], path)
			item_list.append({"link" : path, 
				"id" : str(md5sum.hexdigest()),
				"mediatype" : "image/jpeg",
				"href" : path})
		result += line
	return result, item_list

def fetch_url(url):
	feed = feedparser.parse(url)
	feed_items = feed['items']
	#print feed['channel']['title']
	feed_item_list = { 'title' : feed['channel']['title'], 'items' : [] }
	item_list = []
	for feed_item in feed_items:
		#cur.execute('select * from RSSItems where ItemLink = "%s"', item['link'])

		#if cur.rowcount == 0:
		#	args = (feed['url'], item['title'], item['link'], time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']))
		#	cur.execute('insert into RSSItems (RSSFeedURL, ItemTitle, ItemLink, ItemPubDate) values \
		#		("%s", "%s", "%s", %s)', args)
		#else:
		#	generateHTML(item)

		contents = feed_item.get('content')
		if contents != None:
			for content in contents:
				covert_html = download_url(content['value'])
				content['value'], download_item_list = covert_html
				item_list = item_list + download_item_list
		item_list.append(generateHTML(feed_item))

		'''item_list['items'].append(item['title'].replace('/', '\\') + '.html')
		pattern = re.compile(r'src=')
		contents = item.get('content')
		for content in contents:
			match = pattern.match(content['value'])
			if match:
				print match.group()'''
	json_file = open("item_list.json", "w")
	json.dump(item_list, json_file)
	#json_file.write(str(item_list))
	json_file.close()
	feed_item_list['items'] = item_list
	return feed_item_list

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
	#md5sum = md5()
	result = '''<manifest>\n<item href="css/main.css" id="css" media-type="text/css"/>\n'''
	#item_list = []
	for href in href_list:
		result += '<item href=\"' + href.get('href') + '\" media-type=\"' + href.get('mediatype', "\"application/xhtml+xml\"") + '\" id=\"' + href.get("id") + '\"/>\n'
	result += "<item href=\"RSS4Kindle.ncx\" media-type=\"application/x-dtbncx+xml\" id=\"ncx\" />\n"
	result += "</manifest>\n"
	#print generate_spine(item_list)
	return result

def generate_spine(item_list):
	result = "<spine toc=\"ncx\">\n"
	for item in item_list:
		if item.get("mediatype") == "application/xhtml+xml":
			result += '<itemref idref=\"' + item.get("id") + '\" />\n'
	result += "</spine>\n"
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

def test_generate_ncx(item_tree):
	result = ""
	playOrder = 0
	for tag_tree in item_tree:
		result += '<navPoint id=\"' + tag_tree['id'] + '\" playOrder=\"' + str(playOrder) + '\">\n'
		result += '<navLabel><text>' + tag_tree['tag'] + '</text></navLabel>\n'
		result += '<content src="' + tag_tree['content'] + '"/>\n'
		playOrder = playOrder + 1
		#print tag_tree['tag']
		for RSSFeed_tree in tag_tree['RSSFeeds']:
			result += '<navPoint id=\"' + RSSFeed_tree['id'] + '\" playOrder=\"' + str(playOrder) + '\">\n'
			result += '<navLabel><text>' + RSSFeed_tree['title'] + '</text></navLabel>\n'
			result += '<content src="' + RSSFeed_tree['url'] + '"/>\n'
			for item in RSSFeed_tree['items']:
				result += '<navPoint id=\"' + item['id'] + '\" playOrder=\"' + str(playOrder) + '\">\n'
				result += '<navLabel><text>' + item['title'] + '</text></navLabel>\n'
				result += '<content src="' + item['link'] + '"/>\n'
				result += '</navPoint>\n'
			result += '</navPoint>\n'
			#print RSSFeed_tree['url']
		result += '</navPoint>\n'
	print result

def generate_contain(opf_path):
	container = open(META_INF + "/container.xml", "w")
	container.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
	container.write("<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">\n")
	container.write("<rootfiles>\n")
	container.write("<rootfile full-path=\"" + opf_path + "\" media-type=\"application/oebps-package+xml\"/>\n")
	container.write("</rootfiles>\n")
	container.write("</container>\n")
	container.close()

def generate_files():
	pass

def test():
	json_file = file("../test/test_generate_ncx.json")
	item_tree = json.load(json_file)

	test_generate_ncx(item_tree)


href_list = [{'href' :"1.html", 'mediatype' : "\"application/xhtml+xml\""}, {'href' : "2.html", 'mediatype' : "\"application/xhtml+xml\""}, {'href' : "3.html", 'mediatype' : "\"application/xhtml+xml\""}]
#print generate_manifest(href_list)
feed_item_list = fetch_url('http://coolshell.cn/feed')
opf_head = '''<?xml version="1.0" encoding="UTF-8" ?>
<package version="2.0" unique-identifier="PrimaryID" xmlns="http://www.idpf.org/2007/opf">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
<dc:title> RSS everyday </dc:title>
<dc:identifier opf:scheme="URI" id="etextno">http://www.wyunchilovechina.com/RSS4Kindle/20130825</dc:identifier>
<dc:language>zh_CN</dc:language>
<dc:creator> RSS4Kindle </dc:creator>
<dc:publisher> RSS4Kindle </dc:publisher>
<dc:description> This is description </dc:description>
<dc:coverage></dc:coverage>
<dc:source>www.wyunchilovechina.com</dc:source>
<dc:date>''' + str(datetime.datetime.now())[0 : 19] + '''</dc:date>
<dc:rights> This book is generated from RSS4Kindle </dc:rights>
<dc:subject></dc:subject>
<dc:contributor></dc:contributor>
<dc:type>[type]</dc:type>
<dc:format></dc:format>
<dc:relation></dc:relation>
</metadata>\n\n'''
manifest = generate_manifest(feed_item_list['items'])
spine = generate_spine(feed_item_list['items'])
guide = '''<guide>
</guide>\n'''
opf_file = open(OPS + "/RSS4Kindle.opf", "w")
opf_file.write(opf_head)
opf_file.write(manifest)
opf_file.write(spine)
opf_file.write(guide)
opf_file.write("</package>\n")
#print spine
#print manifest
generate_contain("OPS/RSS4Kindle.opf")

#test()

#cur.close()
#mysql_connection.commit()
#mysql_connection.close()