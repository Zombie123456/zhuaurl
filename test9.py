import requests
from pyquery import PyQuery as pq
from urllib.parse import urlparse
import multiprocessing
import csv
import time


hearders = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	}
a_url = ['baidu', 'news', 'sike', 'qq', 'hao123', 'sport', 'sina', 'worldbank', 
'tuniu', 'liepin', '163', 'org', 'gov', 'net', '666c', 'eastmoney', 'fashion', 
'hotel', 'bbs', 'job', 'people', 'money', 'unionpay', 'ticket', 'ali', 'dujia', 'miss']


def get_data(url):
	try:
		res = requests.get(url, headers=hearders, timeout=5)
	except:
		pass
	else:
		if res.status_code == 200:
			res.encoding = res.apparent_encoding
			return res.text


def parse_data(url, html, l, d, n):
	doc = pq(html)
	aes = doc('a').items()
	list_link = []
	for a in aes:
		if '<img' in a.__str__():
			s = a.attr("href")
			if s:
				if s.startswith('http'):
					res=urlparse(s)
					if res.scheme and res.hostname:
						s56 = f'{res.scheme}://{res.hostname}'
					if res.port:
						s56 = f'{s56}:{res.port}'
					if s56 not in list_link:
						list_link.append(s56)
	l.acquire()
	for item in list_link:
		ppww = True
		for uuu1 in a_url:
			if uuu1 in item:
				ppww = False
				break
		if ppww:
			if item in d:
				d[item] += 1
			else:
				d[item] = 1
	l.release()
	if n == 0:
		return
	wwww = 5
	iframe = doc('iframe').items()
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
			s = parse_data(url, data, l, d, n-1)
		wwww -= 1
		if wwww == 0:
			break


def get_url(file):
	l = []
	with open(file, 'rb') as f:
		for url in f:
			p = True
			try:
				s_url = url.decode()
			except Exception as e:
				print(e)
				continue
			else:
				for i in a_url:
					if i in s_url:
						p = False
						break
				if p:
					if s_url.startswith('http'):
						l.append(s_url.strip('/\r\n'))
					else:
						l.append('http://' + s_url.strip('/\r\n'))
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
			d = sorted(d.items(), key = lambda item:item[1], reverse = True)
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


def main():
	pool = multiprocessing.Pool(processes=4)
	manager = multiprocessing.Manager()
	l = manager.Lock()
	d = manager.dict()
	file = r'./yuan.txt'
	url_l = get_url(file)
	rrrr = 1
	for i in url_l:
		pool.apply_async(run, (i, l, d, rrrr))
		rrrr += 1
	del url_l
	pool.close()
	pool.join()
	d = sorted(d.items(), key = lambda item:item[1], reverse = True)
	open_file(d)
	# send_file('./result.csv')

if __name__ == '__main__':
	print(time.time())
	main()
	print(time.time())





