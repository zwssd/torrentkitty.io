from urllib import parse
import datetime
import requests
import urllib
import os
from os import path
from pathlib import Path
import sys
import time
import math
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_EXCEPTION, ALL_COMPLETED, as_completed
import threading
import socket

class download_m3u8:
	thread_num = 100
	count = 0
	def get_url_list(self, host, body):
		lines = body.split(str.encode('\n'))
		ts_url_list = []
		for line in lines:
			if not line.startswith(str.encode('#')) and line.decode('utf-8') != '':
				if line.startswith(str.encode('http')):
					ts_url_list.append(line)
				else:
					ts_url_list.append('%s/%s' % (host, line.decode('utf-8')))
				#print('line=====>>>>> %s/%s', host, line.decode('utf-8'))
		return ts_url_list

	def get_host(self,url):
		url_base = url[0:url.rfind('/')]
		return url_base

	def get_m3u8_body(self, url, download_path, file_name):
		url = url[0:url.rfind('m3u8')+4]
		print('read m3u8 file:', url)
		session = requests.Session()
		adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=10)
		session.mount('http://', adapter)
		session.mount('https://', adapter)
		r = session.get(url, timeout=10)

		curr_path = download_path + "/{0}.m3u8".format(file_name)
		with open(curr_path, "wb") as code:
			if file_name != 'index':
				lines = r.content.decode()
				print('lines=====>>>>>{0}'.format(lines))
				lines = lines.split('\n')
				for line in lines:
					if line.find('.m3u8') != -1:
						line = file_name + '/index.m3u8'
					#print('line=====>>>>>{0}'.format(line))
					line = line + '\n'
					code.write(line.encode())
			else:
				code.write(r.content)
		return r.content

	'''def download_ts_file(self, ts_url_list, download_dir):
		i = 0
		for ts_url in reversed(ts_url_list):
			i += 1
			file_name = ts_url[ts_url.rfind('/'):]
			curr_path = '%s%s' % (download_dir, file_name)
			print('\n[process]: %s/%s' % (i, len(ts_url_list)))
			print('[download]:', ts_url)
			#print('[target]:', curr_path)
			if os.path.isfile(curr_path):
				print('[warn]: file already exist')
				continue
			urllib.request.urlretrieve(ts_url, curr_path)'''

	# 利用urllib.request.urlretrieve()下载文件
	def download(self, start, end, urls, download_path):
		file_name = start
		for i in urls[start:end]:
			#print('file_name=====%s' % file_name)
			#print(i)
			curr_path = download_path + "/{0}.ts".format(file_name)

			#urllib.request.urlretrieve(i, curr_path)

			session = requests.Session()
			adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=3)
			session.mount('http://', adapter)
			session.mount('https://', adapter)
			r = session.get(i, stream=True, timeout=10)
			with open(curr_path, "wb") as code:
				code.write(r.content)
			self.count += 1
			file_name += 1
			print("下载进度：%.2f" % (self.count / len(urls)), end='\r')


	def download_xcc(self, urls, i, download_path):
		ts_url = urls[i]
		ts_file_name = ts_url[ts_url.rfind('/')+1:]
		curr_path = download_path + "/{0}".format(ts_file_name)

		'''session = requests.Session()
		adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=3)
		session.mount('http://', adapter)
		session.mount('https://', adapter)
		r = session.get(ts_url, stream=True, timeout=8)
		with open(curr_path, "wb") as code:
			code.write(r.content)'''

		# 设置超时时间为30s
		socket.setdefaulttimeout(30)
		# 解决下载不完全问题且避免陷入死循环
		try:
			urllib.request.urlretrieve(ts_url, curr_path)
		except socket.timeout:
			count = 1
			while count <= 5:
				try:
					urllib.request.urlretrieve(ts_url, curr_path)
					break
				except socket.timeout:
					err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
					print(err_info)
					count += 1
			if count > 5:
				print("download job failed!")

		self.count += 1
		print("下载进度：%.2f%%" % (self.count / len(urls) * 100), end='\r')
		return i


	def download_m4a_file(self, url_path, download_path, file_name):
		print("url_path=====>>>>>{0}".format(url_path))
		# 设置超时时间为30s
		socket.setdefaulttimeout(30)
		# 解决下载不完全问题且避免陷入死循环
		try:
			urllib.request.urlretrieve(url_path, download_path+file_name)
		except socket.timeout:
			print("key file download timeout!")
		return 1

	def download_ts_file(self, ts_urls, download_path):
		start_time = time.time()  # 开始时间

		# 利用Python的多线程进行下载
		'''file_size = len(ts_urls)
		part = file_size // self.thread_num
		print('part=====>>>>>\t%d' % part)
		for i in range(self.thread_num):
			start = part * i
			if i == self.thread_num - 1:  # 最后一块
				end = file_size
			else:
				end = start + part
			t = threading.Thread(target=self.download, name='Thread Name %s' % i, kwargs={'start': start, 'end': end, 'urls': ts_urls, 'download_path': download_path})
			t.setDaemon(True)
			t.start()

		while True:
			print('self.count / len(ts_urls) %.6f' % (self.count / len(ts_urls)))
			if math.fabs(self.count / len(ts_urls) - 1.00) < 0.000001:
				break
			else:
				time.sleep(2)'''

		# 等待所有线程下载完成
		'''main_thread = threading.current_thread()
		for t in threading.enumerate():
			if t is main_thread:
				continue
			print("线程名：%s" % t.name)
			t.join()
			print("结束线程名：%s" % t.name)'''

		# 利用Python的线程池进行下载
		with ThreadPoolExecutor(max_workers=100) as t:
			obj_list = []
			for i in range(len(ts_urls)):
				obj = t.submit(self.download_xcc, ts_urls, i, download_path)
				obj_list.append(obj)
			for future in as_completed(obj_list):
				a = 1
				#data = future.result()
				#print(f"main: {data}")

		#future_tasks = [executor.submit(self.download_xcc, ts_urls, i, download_path) for i in range(len(ts_urls))]
		#wait(future_tasks, return_when=ALL_COMPLETED)
		# 等待第一个任务抛出异常，就阻塞线程池
		#wait(task_list, return_when=FIRST_EXCEPTION)
		# 等待正在执行任务执行完成
		#done, unfinished = wait(future_tasks, timeout=800, return_when=ALL_COMPLETED)

		'''for d in done:
			print('执行中:%s, 已完成:%s' % (d.running(), d.done()))
			print(d.result())'''

		# 统计所用时间
		end_time = time.time()
		print('Total cost time:=====>>>>>%s' % (end_time - start_time))

	def file_scan(self, path):
		file_list = []
		# 生成器
		for root, dirs, files in os.walk(path):
			for fn in files:
				p = str(root+'/'+fn)
				file_list.append(p)
		return file_list

	def del_files_dir(self, path):
		for root, dirs, files in os.walk(path):
			for name in files:
				os.remove(os.path.join(root, name))
				#print("Delete File: " + os.path.join(root, name))
		os.rmdir(path)
		return True

	def combine(self, ts_path, combine_path, file_name):
		start_time = time.time()  # 开始时间
		file_list = self.file_scan(ts_path)
		file_list.sort()
		file_path = combine_path + file_name + '.ts'
		path = os.path.dirname(file_list[0])
		with open(file_path, 'wb+') as fw:
			for i in range(len(file_list)):
				file = path + '/' + str(i) + '.ts'
				#print('i======>>>>>%s', i)
				#print('file_list[i]======>>>>>%s', file_list[i])
				#print('file======>>>>>%s', file)
				my_file = Path(file)
				if my_file.is_file():
					fw.write(open(file, 'rb').read())
		# 统计所用时间
		end_time = time.time()
		print('combine file Total cost time:=====>>>>>%s' % (end_time - start_time))
		self.del_files_dir(ts_path)

	def start_download(self, url, file_dir, file_name):
		if url.find('.m4a') != -1:
			self.download_m4a_file(url,file_dir,file_name)
