[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/153QIOOtBYG0FOmpwp81O7hqWiGgXEs73?usp=sharing)
# **Anue**
## **Category**

|中文|category|
|:---:|:---:|
|即時頭條|headline|
|A股港股|cn_stock|
|外匯|forex|
|台股|tw_stock|
|期貨|future|
|國際股|wd_macro|

```python
from Anue.anue import ANUE_CAT

ANUE_CAT.cat

>>> {'即時頭條': 'headline',
     'A股港股': 'cn_stock',
     '外匯': 'forex',
     '台股': 'tw_stock',
     '期貨': 'future',
     '國際股': 'wd_macro'}
```

## **URL Format**
```python
from Anue.anue import ANUE_URL

ANUE_URL.v3
>>> 'https://news.cnyes.com/api/v3/news/category/{cat}?startAt={t1}&endAt={t2}&limit=30&page={page}'
'''
cat --> Category
t1, t2 --> start, end (timestamp)
page --> page
'''
```

## 抓取Anue
### **STEP 1 設定相關資訊**
```python
from Anue.anue import ANUE

anue = ANUE(category = 'tw_stock',
            period = 2) #最近的2天

'''
from Anue.anue import ANUE_CAT

ANUE_CAT.cat = {'即時頭條': 'headline',
                'A股港股': 'cn_stock',
                '外匯': 'forex',
                '台股': 'tw_stock',
                '期貨': 'future',
                '國際股': 'wd_macro'}
'''
```
### **STEP 2 開始抓取**
#### **`crawler_type='quick'`**
```python
for news in anue.crawler_all():
    print(news)
    print('='*100)
```

#### **`crawler_type='complete'`**
```python
for news in anue.crawler_all(crawler_type='complete'):
    print(news)
    print('='*100)
```