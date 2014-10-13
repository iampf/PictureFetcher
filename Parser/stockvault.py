#!/usr/bin/env python2
#! coding:utf-8

from bs4 import BeautifulSoup as bs
from Parser import GetData, StorePicture
import Queue, os
import threading
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
		print url
		category = 'data/stockvault/' + category
		if not os.path.exists('data'):
			os.mkdir('data')
		if not os.path.exists('data/stockvault/'):
			os.mkdir('data/stockvault/')
		if not os.path.exists(category):
			os.mkdir(category)

		html = GetData(url)
		b = bs(html)

		for item in b.find_all(class_ = 'row_images2'):
			for img in item.find_all('li'):
				#img_url = 'http://www.stockvault.net/' + img.a['sample'].split('/.')[1]
				img_url = 'http://www.stockvault.net' + img.a['sample']
				file_name = category + '/' + img.a['title'] + '.jpg'
				if not os.path.exists(file_name):
					StorePicture(img_url, file_name)



class StockVault:
	def __init__(self, thread_num = 0):
		self.thread_num = thread_num
		self.queue = Queue.Queue()

	def start(self):
		self.getCategory()
		#self.getQueue()

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
		html = GetData('http://www.stockvault.net/')
		b = bs(html)
		categories = b.find(class_='categoryitems')
		
		urls = []
		category = []
		
		for item in categories.find_all('li'):
			urls.append( 'http://www.stockvault.net' + item.a['href'])
			category.append( item.b.get_text())


		for i in range(len(urls)):
			html = GetData(urls[i])
			b = bs(html)
			last = int(b.find(class_='paging_bar').find_all('a')[-1]['href'].split('=')[-1])
			for j in range(last):
				self.queue.put( (category[i], urls[i]+'/?s=v&p='+str(j+1),))

	def getQueue(self):
		while True:
			try:
				category, url = self.queue.get(timeout=1)
			except Queue.Empty:
				return
			print category, url
			self.queue.task_done()

if __name__ == '__main__':
	s = StockVault(thread_num=30)
	s.start()
