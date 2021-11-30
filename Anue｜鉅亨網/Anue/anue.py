import os, re
import datetime
import requests, json
from bs4 import BeautifulSoup

class ANUE_CAT:
	cat = {'即時頭條':'headline',
           'A股港股':'cn_stock',
           '外匯':'forex',
           '台股':'tw_stock',
           '期貨':'future',
           '國際股':'wd_macro'}

class ANUE_URL:

	period = 'startAt={t1}&endAt={t2}&limit=30&page={page}'

	v1 = 'https://api.cnyes.com/media/api/v1/newslist/category/{cat}?' + period
	v3 = 'https://news.cnyes.com/api/v3/news/category/{cat}?' + period

	anue_news = 'https://news.cnyes.com/news/id/{newsId}?exp=a'

class ANUE:

	def __init__(self, category, period):

		self.category = category
		self.period = period

	def period_to_timestamp(period):

		end = datetime.datetime.now()
		start = end - datetime.timedelta(days = period)

		end = round(datetime.datetime.timestamp(end))
		start = round(datetime.datetime.timestamp(start))

		return [start, end]

	def url(self, page):

		t1, t2 = ANUE.period_to_timestamp(self.period)

		url = ANUE_URL.v3.format(cat = self.category, t1 = t1, t2 = t2, page = page)
		
		return url

	def crawler(url):

		r = requests.get(url)

		return json.loads(r.text)

	def crawler_all(self):

		list_info = []

		url = ANUE.url(self, page = 1)
		pages = ANUE.crawler(url)['items']['last_page'] + 1
		
		for page in range(1, pages):
			url = ANUE.url(self, page = page)
			json = ANUE.crawler(url)
			list_info.extend(Clean.json_to_info(json))
		return list_info


class Clean:

	def news_ids(datas):
		news_ids = [news['newsId'] for news in datas]
		return news_ids

	def json_to_info(json_data):
		datas = json_data['items']['data']
		list_dict_news_info = []
		urls = [ANUE_URL.anue_news.format(newsId = news_id) for news_id in Clean.news_ids(datas)]

		for url in urls:
			r = requests.get(url)
			info = Clean.get_text(r.text)
			dict_news_info = { "Date": info[0], 
							   "Title": info[1], 
							   "Tags":info[2], 
							   "text": info[3] }
			list_dict_news_info.append(dict_news_info)

		return list_dict_news_info
	def get_text(text):

		soup = BeautifulSoup(text, 'html.parser')
		P = soup.find_all('p')
		text = ''
		for i,p in zip(range(0,len(P)),P):
			if i >=4:
				text = text + p.getText()
			i += 1
		tags = soup.find_all('a')
		n_tags = []
		for tag in tags:
			if re.match('/tag/', str(tag.get('href'))):
				n_tags.append(str(tag.get('href'))[5:len(str(tag.get('href')))])
		title = soup.find('h1').getText()
		T = soup.find('time')
		Date = datetime.datetime.strptime(T['datetime'], "%Y-%m-%dT%H:%M:%S+08:00")

		return (Date,title,n_tags,text)		





