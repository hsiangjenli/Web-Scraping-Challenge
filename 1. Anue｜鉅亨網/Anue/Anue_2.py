import os 
import datetime

class ANUE_URL:
    v1 = 'https://api.cnyes.com/media/api/v1/newslist/category/{cat}?'
    v3 = 'https://news.cnyes.com/api/v3/news/category/{cat}?'

class crawler_method:


class anue:
    cat = {'即時頭條':'headline',
           'A股港股':'cn_stock',
           '外匯':'forex',
           '台股':'tw_stock',
           '期貨':'future',
           '國際股':'wd_macro'}

    def __init__(self, category, version, period):
        self.category = category
        self.version = version
        self.period = period

    def url(self):
        
        cat = anue.cat
        period = 'startAt={t1}&endAt={t2}&limit=30&page={page}'

        if version == 'v1':
            url = v1.format(cat=cat[self.category]) + period
        elif version =='v3':
            url = v3.format(cat=cat[self.category]) + period
        return url

    def period(duration = 30):
        
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days = duration)
        return [end,start]

    def timestamp(period):
        from datetime import datetime
        time_list = []
        for p in period:
             time_list.append(round(datetime.timestamp(p)))
        return {'startAt':time_list[1],'endAt':time_list[0]}
    def last_page(data):
        return int(data['items']['last_page'])

    def crawler(url):
        import urllib
        import json
        with urllib.request.urlopen(url) as jsonfile:
            data = json.loads(jsonfile.read().decode())
        return data

    def get_text(url):
        import urllib
        from bs4 import BeautifulSoup
        import re
        import datetime
        #post_id = url[1]
        data = urllib.request.urlopen(url)
        soup = BeautifulSoup(data, 'html.parser')
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

    def crawler_all(url,p=7):
        all = []
        post_url = 'https://news.cnyes.com/news/id/{}?exp=a'
        t = anue_news.timestamp(anue_news.period(p))
        t1,t2 = t['startAt'],t['endAt']
        page = anue_news.crawler(url.format(t1=t1,t2=t2,page=1))
        for p in range(1,anue_news.last_page(page)+1):
            data = anue_news.crawler(url.format(t1=t1,t2=t2,page=p))
            urls = [post_url.format(item['newsId']) for item in data['items']['data']]
            for i in range(0,len(urls)):
                get = anue_news.get_text(urls[i])
                mydict = { "Date": get[0], "Title": get[1], "Tags":get[2] , "text": get[3] }
                all.append(mydict)
        return all

if __name__ == '__main__':
    
    anue_news.define_url(version,category)
    anue_news.period(duration)
    anue_news.timestamp(period)
    anue_news.get_text(url)
    anue_news.crawler_all(url,p=7)