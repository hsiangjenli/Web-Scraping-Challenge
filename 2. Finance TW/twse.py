import requests, json, os, time
import pandas as pd

from transform_date import TDate

class TWSE_URL:
	'''定義URL'''
	main_path = 'https://www.twse.com.tw/'
	daily_trading = os.path.join(main_path, 'exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock_code}')
	daily_quotes = os.path.join(main_path, 'exchangeReport/MI_INDEX?response=json&date={date}&type=ALL')
	class demo:
		daily_trading = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210812&stockNo=2330'
		daily_quotes = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20210812&type=ALL'


class TWSE:
	
	"""----個人學習如何使用Class----"""
	"""爬取TWSE(證券交易所的股票資料)"""

	cat = {'抓取每日收盤行情(全部)':'crawler_all()',
		   '抓取個股當月收盤行情':'crawler_stocks()'}

	def __init__(self, period, stock_codes=list, daily_quotes_num=range(1,10)):
		self.period = period
		self.stock_codes = stock_codes
		self.daily_quotes_num = daily_quotes_num
		
		'''daily_quotes_num
		可以選擇要回傳特定的dataframe，用list代替
		'''

	def crawler_all(self):

		'''抓取每日收盤行情(全部)'''

		'''包括{價格指數(臺灣證券交易所), 價格指數(跨市場), 價格指數(臺灣指數公司), 
		報酬指數(臺灣證券交易所), 報酬指數(跨市場), 報酬指數(臺灣指數公司), 
		大盤統計資訊, 漲跌證券數合計, 每日收盤行情(全部)}'''

		'''USAGE-1
		period = ('2021-08-12', '2021-08-14')
		twse = TWSE(period = period)
		dict_dfs_date = twse.crawler_all()
		dict_dfs_date.keys()

		for key in dict_dfs:
    		print(dict_dfs[key])
		'''
		dict_dfs_date = {}
		
		start, end = TDate.str.to_date(self.period[0]), TDate.str.to_date(self.period[1])
		
		while start <= end:
			date = TDate.date.to_string_nospace(start)
			try:
				url = TWSE_URL.daily_quotes.format(date = date)
				data = TWSE.crawler(url)
				dict_dfs = {}
				
				for num in self.daily_quotes_num:
					dict_dfs[num] = Clean.to_df_num(data, num)
					dict_dfs[num]['日期'] = datetime.datetime.date(start)
	
				dict_dfs_date[start.strftime('%Y-%m-%d')] = dict_dfs
				time.sleep(5)
			except KeyError:
				pass

			start = TDate.plus.days(start, delta = 1)

		return dict_dfs_date

	def crawler_stocks(self):

		'''抓取個股當月收盤行情'''

		'''USAGE-1
		from twse import TWSE
		period = (######)
		stock_codes = ['2330','1234']
		twse = TWSE(####, stock_codes = stock_codes)
		dict_dfs = twse.crawler_stocks()
		dict_dfs['2330']
		'''
		'''USAGE-2

		dict_dfs['1234'].to_csv('1234.csv')

		'''

		dict_dfs_stock_codes = {}
		
		for stock_code in self.stock_codes:

			result = pd.DataFrame()
			print(stock_code)

			start, end = TDate.str.to_date(self.period[0]), TDate.str.to_date(self.period[1])

			while start <= end:

				date = TDate.date.to_string_nospace(start)
				url = TWSE_URL.daily_trading.format(date = date, stock_code = stock_code)
				data = TWSE.crawler(url)

				locals()[f'df_{stock_code}'+str(start)] = Clean.to_df(data,
																	  stock_code = stock_code)
				result = result.append(locals()[f'df_{stock_code}'+str(start)])

				print(start, end = ' \n')
				time.sleep(5)
				start = TDate.plus.months(start, delta = 1)

			dict_dfs_stock_codes[stock_code] = result

		return dict_dfs_stock_codes

	def crawler(url):
		r = requests.get(url)
		return r.json()
		

class Clean:
	'''將json轉換成DataFrame'''
	
	def to_df(data, stock_code):
		df = pd.DataFrame(data['data'])
		df.columns = data['fields']
		df['日期'] = df['日期'].apply(Clean.ROC_to_date)
		df = df.applymap(Clean.comma)
		df = df.applymap(Clean.to_float)
		df['股票代碼'] = stock_code

		return df

	def to_df_num(data, num):
		df = pd.DataFrame(data[f'data{num}'])
		df.columns = data[f'fields{num}']

		df = df.applymap(Clean.comma)
		df = df.applymap(Clean.to_float)
		df = df.applymap(Clean.html_format)

		return df

	def to_float(x):
		try:
			return float(x)
		except ValueError:
			return x

	def pct_to_float(x):
		if '%' in x:
			try:
				return float(x.strip('%'))/100
			except ValueError:
				return x	
		else:
			return x	
	
	def comma(x):
		try:
			return str(x).replace(',','')
		except ValueError:
			return x
	def replace_triangle(x):
		list_replace = ['▲','▼']
		try:
			return x.replace(list_replace[0], '').replace(list_replace[1], '')
		except:
			return x
		
	def ROC_to_date(ROC_date):
	    import datetime
	    
	    list_ROC_date = [int(d) for d in ROC_date.split('/')]
	    date = datetime.datetime(list_ROC_date[0]+1911, list_ROC_date[1], list_ROC_date[2])
	    
	    return datetime.datetime.date(date)
	def html_format(x):
		try:
			x = x.replace('<p style= color:green>', '')
			x = x.replace('<p style= color:red>', '')
			x = x.replace("<p style ='color:green'>", '')
			x = x.replace("<p style ='color:red'>", '')
			x = x.replace('</p>', '')
			return x
		except AttributeError:
			return x