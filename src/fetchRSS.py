#!/usr/bin/python
#-*- coding:utf-8 -*-

import feedparser
import codecs
import json

class FetchRSS:
	def FetchURL(url):
		feed = feedparser.parse(url)
		feed_items = feed['items']
	    feed_item_list = { 'url' : url, 'title' : feed['channel']['title'], 'items' : [] }
	    item_list = []
	    for feed_item in feed_items:
	    	contents = feed_item.get('content')
	    	if contents != None:
	    		for content in contents:
	    			covert_html = download_url(content['value'])
	    			content['value'], download_item_list = covert_html
	    			item_list = item_list + download_item_list
	    	item_list.append(generateHTML(feed_item))

	    	#json_file = open("item_list.json", "w")
	    	#json.dump(item_list, json_file)
	    	#json_file.close()
	    	feed_item_list['items'] = item_list
	    return feed_item_list