#!/usr/bin/env python3.4

import requests as req
import sys
from lxml import html

def findBetween(s, first, last):
	try:
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
	except ValueError:
		return ""

visitedUrls = []

def searchDown(url, maxDeep, deepnessLevel = 0):
	if deepnessLevel > maxDeep:
		return maxDeep + 1
	visitedUrls.append(url)
	if 'http://pl.wikipedia.org' not in url:
		url = 'http://pl.wikipedia.org' + url

	try:
		code = req.get(url)
	except KeyboardInterrupt:
		exit()
	except:
		print ("Unexpected error: {}".format(sys.exc_info()[0]))
		return maxDeep

	for i in range(deepnessLevel):
		print("\t", end = "")
	print(code.url)
	
	article = findBetween(code.text, '<div id="bodyContent" class="mw-body-content">', '<div id="mw-navigation">')
	webpage = html.fromstring(article)

	links = webpage.xpath("//a/@href")
	
	if '/wiki/Adolf_Hitler' in links:
		return -deepnessLevel
	else:
		lowest = maxDeep
		for link in links:
			if link in visitedUrls:
				continue
			if '.org/wiki' in link:
				continue
			if 'pl.wikiquote.org' in link:
				continue
			if '/wiki' not in link:
				continue
			if ':' in link:
				continue
			if '/wiki/Specjalna:' in link:				
				continue
			if '/wiki/Wikipedia:' in link:
				continue
			if '#' in link:
				continue
			if '/wiki/Szablon:' in link:
				continue
			if '/wiki/Plik:' in link:
				continue
			tmp = searchDown(link, maxDeep, deepnessLevel + 1)
			if tmp < 0:
				if deepnessLevel == 0:
					return -tmp
				else:
					return tmp
			if tmp < lowest:
				lowest = tmp

		return lowest

if len(sys.argv) < 2:
	print("\n\nWynik: {}".format(searchDown('http://pl.wikipedia.org/wiki/Specjalna:Losowa_strona', 4)))
else:
	print("\n\nWynik: {}".format(searchDown(sys.argv[1], 4)))
#print("\n\nWynik: {}".format(searchDown('http://pl.wikipedia.org/wiki/Polacy', 2)))
