# Source 
```python
from twse import TWSE_URL

TWSE_URL.demo.daily_trading
TWSE_URL.demo.daily_quotes
```

# Import TWSE

## Category
```python
from twse import TWSE
TWSE.cat
```

## 抓取每日收盤行情
### STEP 1 設定相關資訊

```python
period = ('2021-08-12', '2021-08-14')

'''方法1'''
daily_quotes = TWSE(period = period)

'''方法2'''
daily_quotes = TWSE(period = period, 
                    daily_quotes_num = [9] # 指定回傳特定資料表, type = list
                   )
```
### STEP 2 開始抓取資料

```python
dict_dfs = daily_quotes.crawler_all()
```

### STEP 3 回傳資料型態

```python
type(dict_dfs)
>>> dict

dict_dfs.keys()
>>> dict_keys(['2021-08-12', '2021-08-13'])

'''
2021-08-14為假日，自動跳過。
'''

for key in dict_dfs['2021-08-12']:
    print(key)

>>> 1 # 110年08月12日 價格指數(臺灣證券交易所)
>>> 2 # 價格指數(跨市場)
>>> 3 # 價格指數(臺灣指數公司)
>>> 4 # 報酬指數(臺灣證券交易所)
>>> 5 # 報酬指數(跨市場)
>>> 6 # 報酬指數(臺灣指數公司)
>>> 7 # 110年08月12日 大盤統計資訊
>>> 8 # 漲跌證券數合計
>>> 9 # 110年08月12日每日收盤行情(全部)
```

```python
daily_quotes = TWSE(period = period, daily_quotes_num = [9])
```

```python
dict_dfs = daily_quotes.crawler_all()
```

```python
dict_dfs['2021-08-13'][9].head(3)
```
## 抓取個股當月收盤行情
### STEP 1 設定相關資訊
```python
stock_codes = ['2330', '1234']
period = ('2021-04-1', '2021-08-1')

'''Period Fomat

   (%Y-%m-%1) 每個月的1號開始及結束，避免重複抓取

'''

twse = TWSE(period = period, stock_codes = stock_codes)
```
### STEP 2 開始抓取資料
#### 方法 1 全部回傳
```python
twse = TWSE(period = period, stock_codes = stock_codes)
dict_dfs = twse.crawler_stocks()
dict_dfs[stock_codes[0]]
```
#### 方法 2 批次回傳
```python
for stock_code in stock_codes:
    twse = TWSE(period = period, stock_codes = [stock_code])
    df = twse.crawler_stocks()
    
df[stock_code]
```
### STEP 3 回傳資料型態
```python
type(dict_dfs)
>>> dict

dict_dfs.keys()
>>> dict_keys(['2330', '1234'])
```
## SQlite
### Table Structure
```python
def create_table():
    tb = '''
            股票代碼 int,
            日期 date, 
            成交股數 float, 
            成交金額 float, 
            開盤價 float, 
            最高價 float, 
            最低價 float, 
            收盤價 float, 
            漲跌價差 float, 
            成交筆數 float    
    '''
    return tb
```

### DB connection
```python
import sqlite3

conn = sqlite3.connect('TWSE.db')
c = conn.cursor() 
try:
    c.execute(f'''CREATE TABLE TWSE({create_table()})''')
except:
    pass
```

```python
from twse import TWSE

period = ('2021-03-1', '2021-08-1')
```

### 存入多筆資料

```python
stock_codes = ['2330','1234', '2357', '2317']

for stock_code in stock_codes:
    twse = TWSE(period = period, stock_codes = [stock_code])
    df = twse.crawler_stocks()
    df[stock_code].to_sql('TWSE', conn, if_exists='append', index = False)
conn.close()
```
### 讀取資料
```python
import sqlite3 as sql
import pandas as pd
con = sql.connect("TWSE.db")
df = pd.read_sql(f"select 股票代碼, 開盤價, 最低價, 最高價, 收盤價, 日期 from TWSE where 股票代碼 = '2330' and 日期 between '2021-08-01' and '2021-08-17'", con)
conn.close
```