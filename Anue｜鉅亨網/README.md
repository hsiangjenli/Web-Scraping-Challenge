# **Anue**
> ð« **åæè²å­¸ç¿ï¼åå¿ç¨ä½åæ¥­ç¨é**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/153QIOOtBYG0FOmpwp81O7hqWiGgXEs73?usp=sharing)
## **Category**

|ä¸­æ|category|
|:---:|:---:|
|å³æé ­æ¢|headline|
|Aè¡æ¸¯è¡|cn_stock|
|å¤å¯|forex|
|å°è¡|tw_stock|
|æè²¨|future|
|åéè¡|wd_macro|

```python
from Anue.anue import ANUE_CAT

ANUE_CAT.cat

>>> {'å³æé ­æ¢': 'headline',
     'Aè¡æ¸¯è¡': 'cn_stock',
     'å¤å¯': 'forex',
     'å°è¡': 'tw_stock',
     'æè²¨': 'future',
     'åéè¡': 'wd_macro'}
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

## æåAnue
### **STEP 1 è¨­å®ç¸éè³è¨**
```python
from Anue.anue import ANUE

anue = ANUE(category = 'tw_stock',
            period = 2) #æè¿ç2å¤©

'''
from Anue.anue import ANUE_CAT

ANUE_CAT.cat = {'å³æé ­æ¢': 'headline',
                'Aè¡æ¸¯è¡': 'cn_stock',
                'å¤å¯': 'forex',
                'å°è¡': 'tw_stock',
                'æè²¨': 'future',
                'åéè¡': 'wd_macro'}
'''
```
### **STEP 2 éå§æå**
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