import scrapy

# 本爬蟲原來是爬 udemycoupon.discountsglobal.com ，因該網站已停止更新，拿來回收再利用
class Uspider03Spider(scrapy.Spider):
    name = 'uspider03'
    allowed_domains = ['www.onlinecourses24x7.com']
    start_urls = ['https://www.onlinecourses24x7.com/']
    
    COUNT_MAX = 15
    count = 0
    
    def parse(self, response):
        items = response.xpath('//*[@class="entry-title"]/a/@href').extract()  # 該頁面所有的文章連結
        for item in items:
            url = response.urljoin(item)
            yield scrapy.Request(url, callback=self.parse_url)
            
        if (self.count < self.COUNT_MAX):  # 如果沒超過設定上限，就繼續爬下一頁
            next_page_url = response.xpath('//*[@class="previous"]/a/@href').extract_first()
            yield scrapy.Request(next_page_url)
            
    def parse_url(self, response):  # 取得每一個 udemy 課程的 url
        title = response.xpath('//*/h1/text()').extract_first()
        
        time = response.xpath('//time[@class="entry-date published"]/@datetime').extract_first()
        time = time[:-15]  # "2021-05-21T18:39:18+01:00" to "2021-05-21"
        
        udemy_url = response.xpath('//*[@class="su-button-center"]/a/@href').extract_first()
        # 移除廣告碼
        udemy_url = udemy_url.replace('https://click.linksynergy.com/deeplink?id=KLRB8G/RnDE&mid=39197&u1=vini&murl=', '')
        udemy_url = udemy_url.replace('%3A', ':')
        udemy_url = udemy_url.replace('%2F', '/')
        udemy_url = udemy_url.replace('%3F', '?')
        udemy_url = udemy_url.replace('%3D', '=')

        tag_list = response.xpath('//*[@class="tag-links"]/a/text()').extract()
        tags = ''.join(str(e) for e in tag_list)  # from list to string 

        self.count = self.count + 1
            
        yield {
            'Count':  self.count,
            'Source':  "3",
            'Title': title,
            'Time': time,
            'UdemyURL': udemy_url,
            'Tags': tags
        }
