import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

baseURL = 'https://megamarket.ru'
target = "iphone-15-pro"
targetURL = baseURL + '/catalog/?q=' + target.replace(' ', '%20')


def get_source_html(url):
    logging.info(f'Opening URL: {url}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        driver.get(url=url)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "html")))
        # Scroll down to load dynamic content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # wait for the page to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

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


def get_items(page_source):
    logging.info('Parsing HTML content.')
    soup = BeautifulSoup(page_source, 'html.parser')
    # Уточнение классов для поиска элементов
    items_divs = soup.find_all('div', class_='catalog-item')
    
    items = {}
    for item in items_divs:
        item_title = item.find('a', class_='catalog-item__name')
        if item_title:
            title = item_title.get_text().strip()
            link = baseURL + item_title.get('href')
            item_price = item.find('span', class_='catalog-item__price-value')
            item_price_result = item_price.get_text().strip() if item_price else 'No price info'
            item_bonus = item.find('span', class_='catalog-item__bonus')
            bonus_text = item_bonus.get_text().strip() if item_bonus else 'No bonus info'
            item_rating = item.find('span', class_='catalog-item__rating')
            rating_text = item_rating.get_text().strip() if item_rating else 'No rating info'
            
            items[link] = {'title': title, 'price': item_price_result, 'bonus': bonus_text, 'rating': rating_text}
            logging.info(f'Item added: {items[link]}')

    logging.info('Items parsed successfully.')
    return items


def output(items):
    logging.info('Outputting items:')
    for link, details in items.items():
        logging.info(f'{link} - {details}')
        print(f'{link} - {details}')


def main():
    logging.info('Script started.')
    page_source = get_source_html(url=targetURL)
    if page_source:
        items = get_items(page_source)
        output(items)
    logging.info('Script finished.')


if __name__ == '__main__':
    main()
