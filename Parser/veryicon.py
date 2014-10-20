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
		category = 'data/veryicon/' + category
		if not os.path.exists('data'):
			os.mkdir('data')
		if not os.path.exists('data/veryicon/'):
			os.mkdir('data/veryicon/')
		if not os.path.exists(category):
			os.mkdir(category)
		html = GetData(url)
		b = bs(html)
		urls = []
		for u in b.find_all(class_='title'):
			urls.append('http://www.veryicon.com' + u.a['href'])
			#print 'http://www.veryicon.com' + u.a['href']
		for u in urls:
			html = GetDate(u)
			b = bs(html)
			for img in b.find_all('a'):
				if '/icon/png' in img['href']:
					print img['href']
					break


		#for u in urls:
			
			

		'''
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
		'''


class VeryIcon:
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
		html = GetData('http://www.veryicon.com/icons/')
		b = bs(html)
		categories = b.find_all('dd')[1:-2]
		urls = []
		category = []
		for item in categories:
			urls.append('http://www.veryicon.com'+item.a['href'])
			category.append(item.a.text.split('(')[0].rstrip())


		for i in range(len(urls)):
			html = GetData(urls[i])
			b = bs(html)
			c = b.find_all(class_='blue')
			for url in c:
				 self.queue.put( (category[i], 'http://www.veryicon.com' + url['href'], ) )

		'''
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
		'''

	def getQueue(self):
		while True:
			try:
				category, url = self.queue.get(timeout=1)
			except Queue.Empty:
				return
			print category, url
			self.queue.task_done()

if __name__ == '__main__':
	s = VeryIcon(thread_num=20)
	s.start()
	'''
	s = VeryIcon(thread_num=30)
	s.getCategory()
	s.getQueue()
	'''
