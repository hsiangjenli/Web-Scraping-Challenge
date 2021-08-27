import requests 
from bs4 import BeautifulSoup

class UDEMY_URL:
	main_path = "https://www.onlinecourses24x7.com/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

class udemy:
	def crawler():
		r = requests.get(UDEMY_URL.main_path, headers = headers)
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



