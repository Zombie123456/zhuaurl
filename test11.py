import requests
from pyquery import PyQuery as pq
from urllib.parse import urlparse
import multiprocessing
import csv
import time


hearders = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	}
a_url = ['baidu', 'news', 'sike', 'qq', 'hao123', 'sports', 'sina']


def get_data(url):
	try:
		res = requests.get(url, headers=hearders, timeout=5)
	except:
		pass
	else:
		if res.status_code == 200:
			res.encoding = res.apparent_encoding
			return res.text


def parse_data(url, html, l, d, n, iframe=''):
	doc = pq(html)
	aes = doc('a').items()
	list_link = []
	for a in aes:
		s = a.attr("href")
		if s and s.startswith('http'):
			list_link.append(s)
	List_set = set(list_link)
	qq = False
	nnnn = 500
	for u in List_set:
		nnnn -= 1
		for fi_url in URL:
			if fi_url in u:
				l.acquire()
				d.append((url, len(List_set), fi_url, iframe))
				l.release()
				qq = True
				break
		if qq or nnnn == 0:
			break
	if n == 0:
		return
	iframe = doc('iframe').items()
	www = 3
	for i in iframe:
		src = i.attr('src')
		if src.startswith('/'):
			src = url + src
		elif src.startswith('http'):
			pass
		else:
			src = url + '/' + src
		data = get_data(src)
		if data:
			s = parse_data(url, data, l, d, n-1, iframe=src)
		www -= 1
		if www == 0:
			break


def get_url(file, http=True):
	l = []
	with open(file, 'rb') as f:
		for url in f:
			p = True
			try:
				s_url = url.decode()
			except Exception as e:
				continue
			else:
				for i in a_url:
					if i in s_url:
						p = False
						break
				if p:
					if http:
						if s_url.startswith('http'):
							l.append(s_url.strip('/\r\n'))
						else:
							l.append('http://' + s_url.strip('/\r\n'))
					else:
						l.append(s_url.strip('/\r\n'))
	return l


def open_file(data):
	file = "./result.csv"
	csvFile = open(file, "w")
	writer = csv.writer(csvFile)
	for i in data:
		writer.writerow(i)
	csvFile.close()


def run(i, l, d, LEN):
	data = get_data(i)
	if data:
		dic = parse_data(i, data, l, d, 1)
	if LEN % 1000 == 0:
		if d:
			open_file(d)
		else:
			open_file([('nodata', '2222')])
		send_file('./result.csv', pppp=False)

def send_file(file, pppp=True):
	url = 'https://api.telegram.org/bot711166180:AAErNuMGY5LU72YP7ZeOBwH53jRKSp5NeXY/sendDocument'
	files = {"document" : open(file)}
	if pppp:
		data = {'chat_id': -398945112}
	else:
		data = {'chat_id': -285548732}
	res = requests.post(url, data=data, files=files)
	print(res.text)


URL = get_url('./shai.txt', False)

def main():
	pool = multiprocessing.Pool(processes=4)
	manager = multiprocessing.Manager()
	l = manager.Lock()
	d = manager.list()
	file = r'./yuan.txt'
	url_l = get_url(file)
	rrr = 1
	for i in url_l:
		pool.apply_async(run, (i, l, d, rrr))
		rrr += 1
	del url_l
	pool.close()
	pool.join()
	d = sorted(d, key = lambda item:item[1], reverse = True)
	open_file(d)
	send_file('./result.csv')

if __name__ == '__main__':
	print(time.time())
	main()
	print(time.time())

