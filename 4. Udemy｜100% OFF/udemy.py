import requests 
from bs4 import BeautifulSoup

class UDEMY_URL:
	main_path = "https://www.udemyfreebies.com"
	page = "/course-category/{category}/{page}"
	url = main_path + page
	second_path = "https://www.onlinecourses24x7.com/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

class UDEMY():
	def __init__(self, category=None, limit_page=7):

		self.limit_page = limit_page

		if category == None:
			self.category = ['Business',
							 'Design',
	 						 'Development',
	 						 'Finance & Accounting',
	 						 'Health & Fitness',
	 						 'IT & Software',
	 						 'Lifestyle',
	 						 'Marketing',
	 						 'Music',
	 						 'Office',
	 						 'Productivity',
	 						 'Personal',
	 						 'Development',
	 						 'Photography',
	 						 'Photography & Video',
	 						 'Teaching & Academics']
		else:
			self.category = category

	def crawler(self):

		category = self.category
		cat1 = category[0]

		valid_urls = []

		r = requests.get(UDEMY_URL.url.format(category = cat1, page = 1),
						 headers = headers)
		soup = BeautifulSoup(r.text, 'lxml')
		valid_urls.extend(UDEMY.find_valid_url(soup))
		last_page = UDEMY.last_page(soup=soup)
		
		list_urls = []
		for cat in category:
			
			valid_urls.extend(UDEMY.find_all_pages_urls(self, last_page = last_page, cat = cat))
		

		for url in valid_urls:
			list_urls.append(UDEMY.go_to_udemy(url=url))
				
		return list_urls
			


	def last_page(soup):

		return soup.find_all('li')[-2].a.text


	def find_valid_url(soup):

		urls = soup.find_all('a', class_='button-icon')
		valid_urls = [url['href'] for url in urls if url.span.text =='Coupon Detail']

		return valid_urls


	def find_all_pages_urls(self, last_page, cat):

		if self.limit_page == None:
			last_page = int(last_page)

		else:
			last_page = self.limit_page

		valid_urls = []

		for page in range(2, last_page + 1):

			r = requests.get(UDEMY_URL.url.format(category = cat, page = page),
							 headers = headers)
			soup = BeautifulSoup(r.text, 'lxml')
			valid_urls.extend(UDEMY.find_valid_url(soup))

		return valid_urls

	def go_to_udemy(url):
		r = requests.get(url, headers = headers)
		soup = BeautifulSoup(r.text, 'lxml')
		uurl = soup.find_all('a', class_ = 'button-icon')[0]['href']
		return uurl



		


class second_udemy:
	def crawler():
		r = requests.get(UDEMY_URL.second_path, headers = headers)
		soup = BeautifulSoup(r.text, 'html.parser')
		h2s = soup.find_all('h2', class_='entry-title')
		titles = [h2.text for h2 in h2s]
		hrefs = [h2.a['href'] for h2 in h2s]
		pub_dates = soup.find_all('time', class_='entry-date published')
		pub_dates = [pub_date['datetime'] for pub_date in pub_dates]
		print(pub_dates)
		list_uedmy_free_urls = []

		for title, href, pub_date in zip(titles, hrefs, pub_dates):
			
			r = requests.get(href, headers = headers)
			soup = BeautifulSoup(r.text, 'html.parser')
			udemy_free_url = soup.find('div', class_='su-button-center').a['href']
			pub_date = soup.find_all('time', class_='entry-date published')
			list_uedmy_free_urls.append({'title':title,
										 'pub_date':pub_date,
										 'url':udemy_free_url})
			
		return list_uedmy_free_urls



