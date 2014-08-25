#!/usr/bin/env python2
import urllib2, urllib

def GetData(url):
	return urllib2.urlopen(url).read()


def StorePicture(url, file_name):
	for i in range(5):
		try:
			urllib.urlretrieve(url, filename=file_name)
			break
		except:
			pass

