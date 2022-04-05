import requests, os, time

from TWSE.transformDate import TDate
from TWSE.Clean import Clean

import datetime as dt

class INDUSTRY:
    Cement = '01'
    Electronic = '13'
    FinancialandInsurance = '17'
    
class TWSE:
    class url:
        main_path = 'https://www.twse.com.tw/'
        DailyTrading = os.path.join(main_path, 'exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock_code}')
        DailyQuotes = os.path.join(main_path, 'exchangeReport/MI_INDEX?response=json&date={date}&type=ALL')
        HighlightsDailyTrading = os.path.join(main_path, 'exchangeReport/FMTQIK?response=json&date={date}')
        TotalIndexHistoricalData = os.path.join(main_path, 'indicesReport/MI_5MINS_HIST?response=json&date={date}')
        DailyIndustry = os.path.join(main_path, 'exchangeReport/MI_INDEX?response=json&date={date}&type={industry_id}')
        Every5SecondsIndex = os.path.join(main_path, 'exchangeReport/MI_5MINS_INDEX?response=json&date={date}')
        class demo:
            '''
            DailyTrading : url
                個股每日收盤行情

            DailyQuotes : url
                全部每日收盤行情
   
            HighlightsDailyTrading : url
                發行量加權股價指數
            '''
            DailyTrading = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210812&stockNo=2330'
            DailyQuotes = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20210812&type=ALL'
            HighlightsDailyTrading = 'https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date=20211213'
            TotalIndexHistoricalData = 'https://www.twse.com.tw/en/indicesReport/MI_5MINS_HIST?response=json&date=20220301'
            Every5SecondsIndex = 'https://www.twse.com.tw/en/exchangeReport/MI_5MINS_INDEX?response=json&date=20220401'

    def __init__(self, period:tuple, stock_codes:list=None, industry_id=None):
        self.period = period
        self.num = [8, 9]
        self.stock_codes = stock_codes
        self.industry_id = industry_id
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
        df : pandas.DataFrame
            回傳每日收盤行情資料.
        '''
        start, end = TDate.str.toDate(self.period[0]), TDate.str.toDate(self.period[1])
        while start <= end:
            if start < dt.datetime(2011, 8, 1):
                num = self.num[0]
            else:
                num = self.num[1]
            
            url = TWSE.url.DailyQuotes.format(date=TDate.date.toStringNospace(start))
            self.crawlerJson(url)
            df = Clean.to_df_num(self.raw, num)
            yield df
            time.sleep(self.sleep)
            start = TDate.plus.days(start, delta = 1)

    def crawlerTaiwanWeightedIndex(self):
        '''
        Parameters
        ----------
        period : Tuple
            從1990-01-04開始提供資料

        Yields
        ------
        df : pandas.DataFrame
            回傳每月發行量加權股價指數資料.

        '''
        start, end = TDate.str.toDate(self.period[0]), TDate.str.toDate(self.period[1])
        while start.year <= end.year:
            if (start.year < end.year) or (start.year == end.year and start.month <= end.month):
                url = TWSE.url.HighlightsDailyTrading.format(date=TDate.date.toStringNospace(start))
                self.crawlerJson(url)
                df = Clean.to_df(self.raw)
                yield df
                time.sleep(self.sleep)
                start = TDate.plus.months(start, delta=1)
            else:
                break
    
    def crawlerIndustry(self):
        start, end = TDate.str.toDate(self.period[0]), TDate.str.toDate(self.period[1])
        num = 1
        while start <= end:
            url = TWSE.url.DailyIndustry.format(date=TDate.date.toStringNospace(start), industry_id=self.industry_id)
            self.crawlerJson(url)
            try:
                df = Clean.to_df_num(self.raw, num)
                df.drop(columns=['漲跌(+/-)'])
                df['日期'] = TDate.date.toStringwithDash(start)
                yield df
            except:
                pass
            time.sleep(self.sleep)
            start = TDate.plus.days(start, delta = 1)        
    
    def crawlerStockDailyTrading(self):
        pass
        
    def crawlerTotalIndexHistoricalData(self):
        start, end = TDate.str.toDate(self.period[0]), TDate.str.toDate(self.period[1])
        while start.year <= end.year:
            if (start.year < end.year) or (start.year == end.year and start.month <= end.month):
                url = TWSE.url.TotalIndexHistoricalData.format(date=TDate.date.toStringNospace(start))
                self.crawlerJson(url)
                df = Clean.to_df(self.raw)
                yield df
                time.sleep(self.sleep)
                start = TDate.plus.months(start, delta=1)
            else:
                break
    
    def crawlerEvery5SecondsIndex(self):
        start, end = TDate.str.toDate(self.period[0]), TDate.str.toDate(self.period[1])
        while start <= end:
            url = TWSE.url.Every5SecondsIndex.format(date=TDate.date.toStringNospace(start))
            self.crawlerJson(url)
            try:
                df = Clean.to_df_num(self.raw)
                df['日期'] = TDate.date.toStringwithDash(start)
                yield df
            except:
                pass
            time.sleep(self.sleep)
            start = TDate.plus.days(start, delta = 1)
        
        
            