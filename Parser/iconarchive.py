#!/usr/bin/env python2
#! coding:utf-8

from Parser import GetData, StorePicture
from bs4 import BeautifulSoup as bs
import Queue, threading
import os
class Worker(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	def run(self):
		while True:
			try:
				category, url = self.queue.get(timeout=1)
			except Queue.Empty:
				return
			self.getPicturesFromCategory(category, url)
			self.queue.task_done()


	def getPicturesFromCategory(self, category, url):
		print category
		category = 'data/iconarchive/' + category
		if not os.path.exists('data'):
			os.mkdir('data')
		if not os.path.exists('data/iconarchive'):
			os.mkdir('data/iconarchive')
		if not os.path.exists(category):
			os.mkdir(category)


		html = GetData(url)
		b = bs(html)
		for item in b.find_all(class_='iconset'):
			c_url = 'http://www.iconarchive.com' + item.find(class_='s-preview').find('a')['href']
			c = item.find(class_='s-text').find('h2').get_text()
			if '/' in c:
				c = c.replace('/','_')
			c = category + '/' + c

			if not os.path.exists(c):
				os.mkdir(c)
			self.getPictures(c, c_url)


	def getPictures(self, category, url):
		html = GetData(url)
		b = bs(html)
		for item in b.find_all(class_='lastitem'):
			p_url = item['href']
			file_name = category + '/' + p_url.split('/')[-1]
			if not os.path.exists(file_name):
				StorePicture(p_url, file_name)

class IconArchive:
	def __init__(self, thread_num = 0):
		self.thread_num = thread_num
		self.queue = Queue.Queue()

	def start(self):
		self.getCategory()
		
		threads = []

		for i in range(self.thread_num):
			worker = Worker(self.queue)
			worker.setDaemon(True)
			worker.start()
			threads.append(worker)
		self.queue.join()

		for item in threads:
			item.join()	
				


	def getCategory(self):
		html = GetData('http://www.iconarchive.com/categories.html')
		b = bs(html)
		#category_item = b.find_all(attrs={'class':'category-item'})
		category_item = b.find_all(class_='category-item-link')
		for c in category_item:
			url = 'http://www.iconarchive.com' + c['href']
			data =  c.find('div').find('div').get_text()
			category,num = data.split('(')
			num = int(num.split(' ')[0])
			self.putCategoryURLinQueue(category, num, url)

	def putCategoryURLinQueue(self, category, num, url):
		max = num / 24 + 1
		for i in range(max):
			category_url = url.split('.html')[0] + '.by-date.' + str(i+1) + '.html'
			self.queue.put((category,category_url,))



	def getQueue(self):
		while True:
			try:
				data = self.queue.get(timeout=1)
			except Queue.Empty:
				return
			print data

if __name__ == '__main__':
	a = IconArchive(20)
	a.start()

