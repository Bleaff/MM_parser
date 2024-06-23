import requests
from bs4 import BeautifulSoup
import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ProductParser import ProductParser
import logging

def get_source_html(url):
	logging.info(f'Opening URL: {url}')
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	driver.maximize_window()

	try:
		driver.get(url=url)
		WebDriverWait(driver, 60).until(
			EC.presence_of_element_located((By.TAG_NAME, "html")))
		# Scroll down to load dynamic content

		page_source = driver.page_source
		logging.info('Page source obtained successfully.')
		return page_source
	except Exception as ex:
		logging.error(f'Error while getting page source: {ex}')
		return None
	finally:
		driver.close()
		driver.quit()
		logging.info('Browser closed.')

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

baseURL = 'https://megamarket.ru'
target = "iphone-15-pro"
targetURL = baseURL + '/catalog/?q=' + target.replace(' ', '%20')

def get_items(page_source):
	logging.info('Parsing HTML content.')
	soup = BeautifulSoup(page_source, 'html.parser')
	with open('page_source.html', 'w', encoding='utf-8') as file:
		file.write(soup.prettify())
	# Уточнение классов для поиска элементов
	product_items = soup.find_all('div', {"data-test": "product-item"})
	logging.info(f'Found {len(product_items)} items.')
	return product_items

def main():
	pp = ProductParser
	logging.info('Script started.')
	page_source = get_source_html(url=targetURL)
	product_items = get_items(page_source)
	product_list = []
	for product_item in product_items:
		product = pp.extract_product_data(product_item)
		product_list.append(product)
	if len(product_list) > 0:
		print(product_list[0])
	logging.info('Script finished.')

if __name__ == '__main__':
	main()