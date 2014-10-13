#!/usr/bin/env python2

from bs4 import BeautifulSoup as bs

def tagParser(html, tag):
	b = bs(html)
	return b.find_all(tag)

if __name__ == '__main__':
	print 'Hello'
