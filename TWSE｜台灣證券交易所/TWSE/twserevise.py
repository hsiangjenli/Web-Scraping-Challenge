import requests, os, time

from transform_date import TDate
import datetime

from Clean import Clean

class TWSE:
    class url:
        main_path = 'https://www.twse.com.tw/'
        daily_trading = os.path.join(main_path, 'exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock_code}')
        DailyQuotes = os.path.join(main_path, 'exchangeReport/MI_INDEX?response=json&date={date}&type=ALL')
        HighlightsDailyTrading = os.path.join(main_path, 'exchangeReport/FMTQIK?response=json&date={date}')
        class demo:
            '''
            daily_trading : url
                個股每日收盤行情

            daily_quotes : url
                全部每日收盤行情
   
            highlights_daily_Trading : url
                台灣加權指數
            '''
            daily_trading = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210812&stockNo=2330'
            DailyQuotes = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20210812&type=ALL'
            HighlightsDailyTrading = 'https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date=20211213'
            
    class sql:
        createTable = '''
        `證券代號` varchar(20) NOT NULL,
        `證券名稱` varchar(20) NOT NULL,
        `成交股數` float,
        `成交筆數` float,
        `成交金額` float,
        `開盤價` float NOT NULL,
        `最高價` float NOT NULL,
        `最低價` float NOT NULL,
        `收盤價` float NOT NULL,
        `漲跌價差` float,
        `最後揭示買價` float,
        `最後揭示買量` float,
        `最後揭示賣價` float,
        `最後揭示賣量` bigint(20),
        `本益比` float,
        `日期` date NOT NULL
        '''
    def __init__(self, period:tuple, stock_codes=None, date=datetime):
        self.period = period
        self.num = [8, 9]
        self.stock_codes = stock_codes
        self.date = date
        self.sleep = 5

    def crawler_json(self, url):
        '''
        Parameters
        ----------
        url : string
            Target's url.

        Returns
        -------
        self.raw : json
            return json format data from TWSE.
        '''
        try:
            r = requests.get(url)
            self.raw = r.json()
            return self
        except KeyError:
            pass
    def crawlerLoop(self, urlFormat, cleaningMethod):
        '''
        這裡還沒寫完!!!!!!!!!!!!!!!

        Parameters
        ----------
        urlFormat : TYPE
            DESCRIPTION.
        cleaningMethod : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        start, end = TDate.str.to_date(self.period[0]), TDate.str.to_date(self.period[1])
        while start <= end:
            '''
            url = urlFormat # TWSE.url.daily_quotes.format(date=TDate.date.to_string_nospace(start))
            srart = TDate().plus.days(start, delta=1)
            '''
            pass

    def crawlerDailyQuotes(self):
        '''
        Parameters
        ----------
        period : Tuple
            period=('2021-08-11', '2021-08-14')
            
        num : integer
            num=8, 2004-02-11 ~ 2011-08-01
            num=9, 2011-08-02 ~ now

        Yields
        ------
        df : pandas.DataFrame()
            回傳每日收盤行情資料.
        '''
        start, end = TDate.str.to_date(self.period[0]), TDate.str.to_date(self.period[1])
        while start <= end:
            url = TWSE.url.DailyQuotes.format(date=TDate.date.to_string_nospace(start))
            self.crawler_json(url)
            df = Clean.to_df_num(self.raw, self.num[1])
            yield df
            time.sleep(self.sleep)
            start = TDate.plus.days(start, delta = 1)

    def crawlerTaiwanWeightedIndex(self):
        pass
    def crawlerStockDailyTrading(self):
        pass
        
        
            