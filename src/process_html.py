#!/usr/bin/python
#-*- coding:utf-8 -*-

import re
import urllib
from hashlib import md5

file = open("7 CPU sample.html", "rb")
lines = file.readlines()

pattern = re.compile(r'/src=/s')
def suffix(url):
	return url.split('.')[-1]

def download_url(lines):
	md5sum = md5()
	for line in lines:
		#match = pattern.match(line)
		match = re.search(r'src', line)
		if match:
			start = line.find('src="') + 5
			end = line.find('"', start)
			url = line[start : end]
			md5sum.update(url)
			path = str(md5sum.hexdigest()) + "." + suffix(url)
			urllib.urlretrieve(url,path)

file.close()