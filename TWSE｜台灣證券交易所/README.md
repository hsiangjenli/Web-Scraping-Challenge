# **TWSE**

## **使用**

### **基本**

```python
from TWSE.twserevise import TWSE

period = ('2021-08-11', '2021-10-13')
twse = TWSE(period=period)
```

#### **每日收盤行情**

```python
for df in twse.crawlerDailyQuotes():
    print(df)
```

#### **台灣加權價指數**

```python
for df in twse.crawlerTaiwanWeightedIndex():
    print(df)
```

### **連接資料庫**

#### **SQLite**

```python
import sqlite3

table = '發行量加權股價指數'

createTable = '''
    `日期` date NOT NULL,
    `成交股數` bigint(20) NOT NULL,
    `成交金額` bigint(20) NOT NULL,
    `成交筆數` bigint(20) NOT NULL,
    `發行量加權股價指數` DECIMAL(7, 2) NOT NULL,
    `漲跌點數` float NOT NULL
    '''

conn = sqlite3.connect('TWSE.db')
c = conn.cursor() 
try:
    c.execute(f'CREATE TABLE TWWI ({createTable})')
except:
    pass

from TWSE.transformDate import TDate
from TWSE.twserevise import TWSE
import datetime

import numpy as np

now = TDate.date.toStringwithDash(datetime.datetime.now())
#period = ('1990-01-04', now)
#period = (rDate, now)
period = ('2016-10-10', now)
twse = TWSE(period=period)

for df in twse.crawlerTaiwanWeightedIndex():
    df.to_sql(table, con = conn, if_exists = 'append', index=False)
```

#### **MySQL**

```python
from sqlalchemy import create_engine
import MySQLdb

user = 'root'
pw = "****"
db = 'TWSE'
table = '發行量加權股價指數'

createTable = '''
    `日期` date NOT NULL,
    `成交股數` bigint(20) NOT NULL,
    `成交金額` bigint(20) NOT NULL,
    `成交筆數` bigint(20) NOT NULL,
    `發行量加權股價指數` DECIMAL(7, 2) NOT NULL,
    `漲跌點數` float NOT NULL
    '''

engine = create_engine(f'mysql+pymysql://{user}:{pw}@localhost/{db}')
conn=MySQLdb.connect(host="127.0.0.1",user=user, passwd=pw,charset='utf8')
cursor=conn.cursor()
cursor.execute(f'USE {db}')

try:
    cursor.execute(f'CREATE TABLE `{table}` ({createTable})')
except:
    pass

from TWSE.transformDate import TDate
from TWSE.sqlHelper import sqlHelper as sHelper
from TWSE.twserevise import TWSE

import numpy as np

sh = sHelper(user=user, pw=pw, db=db, table=table)
now = TDate.date.toStringwithDash(datetime.datetime.now())
rDate = sh.getResult(rType='string')
#period = ('1990-01-04', now)
#period = (rDate, now)
period = ('2021-10-10', now)
twse = TWSE(period=period)

for df in twse.crawlerTaiwanWeightedIndex():
    if sh.inSql(df):
        if sh.LocList(df) != None:
            df = df.loc[sh.LocList(df)]
        else:
            break
    df.to_sql(table, con = engine, if_exists = 'append', index=False)
```
