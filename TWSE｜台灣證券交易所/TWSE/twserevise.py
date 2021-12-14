import requests, os, time

from TWSE.transformDate import TDate
from TWSE.Clean import Clean

import datetime as dt

class TWSE:
    class url:
        main_path = 'https://www.twse.com.tw/'
        DailyTrading = os.path.join(main_path, 'exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock_code}')
        DailyQuotes = os.path.join(main_path, 'exchangeReport/MI_INDEX?response=json&date={date}&type=ALL')
        HighlightsDailyTrading = os.path.join(main_path, 'exchangeReport/FMTQIK?response=json&date={date}')
        class demo:
            '''
            DailyTrading : url
                個股每日收盤行情

            DailyQuotes : url
                全部每日收盤行情
   
            HighlightsDailyTrading : url
                台灣加權指數
            '''
            DailyTrading = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210812&stockNo=2330'
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
    def __init__(self, period:tuple, stock_codes:list=None):
        self.period = period
        self.num = [8, 9]
        self.stock_codes = stock_codes
        self.sleep = 5

    def crawlerJson(self, url):
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
        start, end = TDate.str.withNospace(self.period[0]), TDate.str.withNospace(self.period[1])
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
        start, end = TDate.str.toDate(self.period[0]), TDate.str.toDate(self.period[1])
        while start <= end:
            if start < dt.datetime(2011, 8, 1):
                num = self.num[0]
            else:
                num = self.num[1]
            
            url = TWSE.url.DailyQuotes.format(date=TDate.date.toStringNospace(start))
            print(url)
            self.crawlerJson(url)
            df = Clean.to_df_num(self.raw, num)
            yield df
            time.sleep(self.sleep)
            start = TDate.plus.days(start, delta = 1)

    def crawlerTaiwanWeightedIndex(self):
        start, end = TDate.str.toDate(self.period[0]), TDate.str.toDate(self.period[1])
        while start.year <= end.year:
            if start.year == end.year and start.month <= end.month:
                url = TWSE.url.HighlightsDailyTrading.format(date=TDate.date.toStringNospace(start))
                self.crawlerJson(url)
                df = Clean.to_df(self.raw)
                yield df
                time.sleep(self.sleep)
                start = TDate.plus.months(start, delta=1)
            else:
                break
        
    def crawlerStockDailyTrading(self):
        pass
        
        
            