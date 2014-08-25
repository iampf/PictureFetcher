#!/usr/bin/env python2
#! coding:utf-8
import urllib2
from tagParser import tagParser
from bs4 import BeautifulSoup as bs
import os
import threading, Queue
from Parser import GetData, StorePicture
class IconFinderWorker(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			try:
				category, url = self.queue.get(timeout=1)
			except Queue.Empty:
				return
			
			icon = IconFinder()
			icon.getPicturesFromCategory(category, url)

			self.queue.task_done()


class IconFinder:
	def __init__(self, thread_num = 0):
		self.url = 'https://www.iconfinder.com/'
		self.data = urllib2.urlopen(self.url).read()
		self.thread_num = thread_num
		self.proxy = []

	def start(self, proxy=None):
		category, urls = self.getCategory()

		if self.thread_num != 0:
						
			queue = Queue.Queue()
			threads = []

			for i in range(self.thread_num):
				worker = IconFinderWorker(queue)
				worker.setDaemon(True)
				worker.start()
				threads.append(worker)

			for i in range(len(urls)):
				queue.put((category[i],urls[i]))
			queue.join()

			for item in threads:
				item.join()

		else:
			for i in range(len(urls)):
				self.getPicturesFromCategory(category[i],urls[i])
	
	def getCategory(self):
		'''
			Get Image's Categories
		'''
		category = []
		urls = []
		b = bs(self.data)
		for i in b.find_all(attrs={'class':'category'}):
			category.append( 'data/iconfinder/' + i.string + '/')
			urls.append( 'https://www.iconfinder.com' + i.a.attrs['href'] )

		return category, urls

	def getPicture(self, category, url):
		html = GetData(url)
		b = bs(html)
		for i in b.find_all('img', attrs={'class':True}):
			file_name = category + '/' + i['src'].split('/')[-1]
			if not os.path.exists(file_name):
				StorePicture(i['src'], file_name)
			

	def getPictures(self, html, category):
		b = bs(html)
		for i in b.find_all('article'):
			c = i.find('h4').a.string
			url = 'http://www.iconfinder.com' + i.find('h4').a['href']
			print category+c
			if not os.path.exists(category+c):
				os.mkdir(category+c)

			self.getPicture( category+c, url)

			
		
	def getPicturesFromCategory(self, category, url):
		'''
			Get Pictures from category
		'''

		# Create Data Directory
		if not os.path.exists('data'):
			os.mkdir('data')
		if not os.path.exists('data/iconfinder'):
			os.mkdir('data/iconfinder')
		if not os.path.exists(category):
			os.mkdir(category)

		for page in range(1,300):
			u = url + '?page=' + str(page)
			data = GetData(u)
			self.getPictures(data, category)
			if data.count('next') <= 1:
				break
			
			
			
		

if __name__ == '__main__':
	
	i = IconFinder(thread_num=20)
	i.start()
	'''
	category, urls = IconFinder().getCategory()
	for j in range(len(category)):
		i.getPicturesFromCategory(category[j],urls[j])
	'''
		
