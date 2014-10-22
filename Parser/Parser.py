#!/usr/bin/env python2
import urllib2, urllib

def GetData(url):
	for i in range(5):
		try:
			return urllib2.urlopen(url).read()
		except:
			pass
	return None


def StorePicture(url, file_name):
	for i in range(5):
		try:
			print url, file_name
			urllib.urlretrieve(url, filename=file_name)
			break
		except Exception, e:
			print url, str(e)
			pass

