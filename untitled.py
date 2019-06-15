import requests
from pyquery import PyQuery as pq
from urllib.parse import urlparse
import multiprocessing
import csv
import time
import warnings
warnings.filterwarnings("ignore")


hearders = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	}
a_url = ['baidu', 'news', 'sike', 'qq', 'hao123', 'sport', 'sina', 'bank', 
'tuniu', 'liepin', '163', 'org', 'gov', 'net', '666c', 'eastmoney', 'fashion', 
'hotel', 'bbs', 'job', 'people', 'money', 'unionpay', 'ticket', 'ali', 'dujia', 'miss', 'voc', 'sohu', 'pingan', '.cn',
'jmw', 'home', 'panjk', 'admaimai', 'zxart', 'gongjiao', 'jiancai', 'blog', '.tw', 'liebiao', '51sole', '591hx', '17house', 'space',
'site', '.ltd', 'dream', 'java', 'sonhoo', 'zhaoshang100', 'chn0769', 'taobao', 'live', '360', 'gx211', 'huangye88', '554757', 'china', 'city', 'chat',
'agent', 'zhuangyi', 'b2b', '99cfw', 'cnjy', 'game', 'ci123', 'house', 'bao315', 'xyj321', 'fenlei', 'mgd', 'kugou', 'bizhi', 'e2say', '54086', 'qy39', 'xyj321', '7999',
'jixiexinxi', '.xyz', 'info', 'car', 'uc', 'shop', 'lin', 'xg557', 'xg67', 'club', '.st', '999677', 'ip', '.pw', 'south', 'redit', 'huanqiu', 'world', 'ganji']

b_url = ['.jpg', '.png', '.gif'
]

# c_choose = ['<img', '立即开户', '立即投注']

c_choose = ['肖', '码', '特', '期', '推荐', '平', '一', '爆', '投资', '绝杀', '计划', '中', 
'心水', '单', '双', '主攻', '赚', '准', '现场', '开奖', '资料', '图解', '玄机', '碼', '推薦','絕殺', '計劃', '圖解','開獎', '現場','賺',
'單', '雙', '準', '資料'
]

def get_data(url):
	try:
		s = requests.Session()
		res = s.get(url, headers=hearders, timeout=(5, 18), verify=False)
		encoding = res.headers.get('content-type', '')[19:]
		if encoding:
			res.encoding = encoding
		else:
			res.encoding = res.apparent_encoding
		return res.text
	except Exception as e:
		print(e)


def parse_data(url, html, l, d, n):
	doc = pq(html)
	aes = doc('a').items()
	list_link = []
	for a in aes:
		if not is_normal(c_choose, a.__str__()):
			s = a.attr("href")
			if s:
				if s.startswith('http'):
					res=urlparse(s)
					try:
						if res.scheme and duje_hostname(res.hostname):
							s56 = f'{res.scheme}://{res.hostname}'
							if res.port:
								s56 = f'{s56}:{res.port}'
							if s56 not in list_link:
								if is_normal(b_url, s):
									list_link.append(s56)
					except Exception as e:
						print(e)
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


def is_normal(choose_list, value):
	for val in choose_list:
		if val in value:
			return False
	return True


def duje_hostname(hostname):
	# if hostname[0].isdigit() and list(hostname).count('.') == 1:
	# 	return True
	# elif hostname[0:3] == 'www':
	# 	for s in hostname[3:]:
	# 		if s.isdigit():
	# 			return True
	# return False
	if '.' in hostname:
		return True
	else:
		return False


def get_url(file):
	l = []
	with open(file, 'rb') as f:
		for url in f:
			try:
				s_url = url.decode()
			except Exception as e:
				print(e)
				continue
			else:
				if is_normal(a_url, s_url):
					if s_url.startswith('http'):
						l.append(s_url.strip('/\r\n'))
					else:
						l.append('http://' + s_url.strip('/\r\n'))
	return l


def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


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
	if LEN % 5000 == 0:
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
	pool = multiprocessing.Pool(processes=8)
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





