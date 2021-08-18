import request, json, time, os, io
import shutil, zipfile
import pandas as pd

from transform_date import TDate
from twse import Clean

class TAIFEX_URL:
	main_path = 'https://www.taifex.com.tw/'

	futures_daily_trading = os.path.join(main_path, 'cht/3/futDailyMarketReport')
	
	options_daily_trading = os.path.join(main_path, 'cht/3/optDailyMarketReport')
	options_daily_marketview = os.path.join(main_path, 'cht/3/optDailyMarketView')
	
	options_daily_trading_summary = os.path.join(main_path, 'cht/3/optDailyMarketSummary')
	options_Previous30Days_SalesData = os.path.join(main_path, 'file/taifex/Dailydownload/OptionsDailydownloadCSV/OptionsDaily_2021_07_29.zip')


class TAIFEX_ID:
	class options:
		commodity_ids = ["RHO", "RTO", "TEO", "TFO", "TGO", "TXO"]
	class futures:
		commodity_ids = ["BRF", "F1F", "GDF", "MTX", "RHF", "RTF", "SPF", "TE", "TGF", "TX", "UDF", "UNF", "XAF", "XBF", "XEF", "XJF", "ZEF"]
	

class crawler_method:
	class options:

		def daily_trading_normal(dfs, start):
			df = dfs[4].iloc[0:-2]
			df = df.applymap(Clean.replace_triangle)
			df = df.applymap(Clean.pct_to_float)
			df = df.applymap(Clean.to_float)
			df['日期'] = datetime.datetime.date(start)	
			return df

		def daily_trading_specialid(dfs, start):
			dfs = dfs[4]
			try:
				split_index = dfs[dfs['契約']=='契約'].index[0]
				df2 = dfs.iloc[(split_index+1):-2]
			except IndexError:
				df2 = dfs.iloc[0:-2]

			df2 = df2.reset_index(drop=True)
			df2 = df2.applymap(Clean.to_float)
			df2['Date'] = start
			#df1 = dfs.iloc[0:(split_index-1)]
			return df2


class TAIFEX:

	'''
	["RHO", "RTO", "TEO", "TFO", "TGO", "TXO"] 不可與股票選擇權混用
	'''

	def __init__(self, 
				 period, 
				 commodity_ids,
				 commodity_id2 = '',
				 market_code = 0):

		self.period = period
		self.market_code = market_code
		self.commodity_id = commodity_ids
		self.commodity_ids = commodity_ids
		self.commodity_id2 = commodity_id2

	def options_daily_trading_form_data(commodity_id, 
										commodity_id2, 
										market_code, 
										date):
		
		'''
		一般交易時段:0
		commodity_id: 指數選代碼
		commodity_id: RHO, RTO, TEO, TFO, TGO, TXO, specialid(代表股票選擇權)

		commodity_id2: 股票選擇權代碼
		'''	

		date = TDate.date.to_string_slash(date)
		
		form_data = {
			'queryType': 2, 
	        'marketCode': market_code, 
	        'dateaddcnt': '', 
	        'commodity_id': commodity_id, 
	        'commodity_id2': commodity_id2, 
	        'queryDate': date, 
	        'MarketCode': market_code, 
	        'commodity_idt': commodity_id, 
	        'commodity_id2t': commodity_id2, 
	        'commodity_id2t2': ''
	        }		
		return form_data

	def options_daily_trading(self):
		commodity_ids = self.commodity_ids
		commodity_id2 = self.commodity_id2

		market_code = self.market_code

		'''commodity_ids == 'specialid'
		   將commodity_ids改成commodity_id2，後面for迴圈才不會出錯。
		   並且在for迴圈裡加入
		   					commodity_id2 = commodity_id
		   					commdity_id = self.commodity_ids
		   最後，放入TAIFEX.options_daily_trading_form_data()
		'''

		if commodity_ids == 'specialid':
			commodity_ids = commodity_id2

		url = TAIFEX_URL.options_daily_trading

		dict_dfs_commodity_ids = {}
		
		for commodity_id in commodity_ids:
			
			start, end = TDate.str.to_date(self.period[0]), TDate.str.to_date(self.period[1])
			
			result = pd.DataFrame()
			if self.commodity_ids == 'specialid':
				commodity_id2 = commodity_id
				commodity_id = self.commodity_ids

			while start <= end:

				form_data = TAIFEX.options_daily_trading_form_data(
											 commodity_id = commodity_id, 
									  		 commodity_id2 = commodity_id2, 
									  		 market_code = market_code,
									  		 date = start)

				r = requests.post(url, form_data)
				dfs = pd.read_html(r.text)

				'''crawler_method.options
				   指數選擇權、股票選擇權Table不同
				'''

				if commodity_id in TAIFEX_ID.options.commodity_ids:
					df = crawler_method.options.daily_trading_normal(dfs, start)

				elif commodity_id == 'specialid':
					df = crawler_method.options.daily_trading_specialid(dfs, start)

				result = result.append(df)
				start = TDate.plus.days(start, delta = 1)

			if commodity_id == 'specialid':
				dict_dfs_commodity_ids[commodity_id2] = result

			elif commodity_id in TAIFEX_ID.options.commodity_ids:
				dict_dfs_commodity_ids[commodity_id] = result

		return dict_dfs_commodity_ids

	def unzip_from(url):

		'''解壓縮檔案'''

		r = requests.get(url)
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall("tempt")

	def create_folder(folder_name):

		'''Create a folder and store all files'''

		if not os.path.exist(folder_name):
			os.mkdir(folder_name)
		else:
			pass

	def move_file(tempt_folder, file_name, folder_name):

		'''將解壓縮完的檔案移動到目的地'''
		'''source --> 檔案原始位置
		   destination --> 目標位置'''

		file_name = 'OptionsDaily_2021_07_29.csv'

		source = os.path.join(tempt_folder, file_name)
		destination = folder_name

		shutil.move(source, destination)

	def remove_tempt_folder(tempt_folder = 'tempt'):

		'''將解壓縮的暫存資料夾刪除'''

		if os.path.exist(tempt_folder):
			os.rmdir(tempt_folder)
		else:
			pass

		