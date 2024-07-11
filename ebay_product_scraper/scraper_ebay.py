import time
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class EbayScraper:
    def __init__(self,url,file_name='index_selenium.html'):
        self.url = url
        self.file_name = file_name
        self.all_products_data=[]


def fetch_page(url, file_name):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url=url)
        time.sleep(1)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
    except Exception as e:
        print(f"Error fetching the page: {e}")
    finally:
        driver.close()
        driver.quit()


def parse_links(file_name):
    list_cards_url = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'html.parser')
        lego_cards = soup.find_all('li', class_="brwrvr__item-card brwrvr__item-card--list")
        for card in lego_cards:
            link = card.find('a').get('href')
            list_cards_url.append(link)
    except Exception as e:
        print(f"Error parsing the file: {e}")
    return list_cards_url


def scrape_product_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1', class_="x-item-title__mainTitle").text.strip()
        seller = soup.find('div', class_="x-sellercard-atf__info__about-seller").text.strip()
        price = soup.find('div', class_="x-price-primary").text.strip()
        shipping_price = soup.find('div', class_="ux-labels-values__values-content").text.strip()
        photo = soup.find('div', class_="ux-image-grid no-scrollbar")
        photo_link = photo.find('img').get('src') if photo else None

        product_data = {
            'Name': name,
            'Product Link': url,
            'Photo Link': photo_link,
            'Price': price,
            'Seller': seller,
            'Shipping Price': shipping_price
        }
        return product_data
    except Exception as e:
        print(f"Error scraping product info for URL {url}: {e}")


def main(url, file_name='index_selenium.html'):
    fetch_page(url, file_name)
    links = parse_links(file_name)

    all_product_data = []
    for link in links:
        product_data = scrape_product_info(link)
        if product_data:
            all_product_data.append(product_data)
            print(json.dumps(product_data, indent=4))
    with open('ebay_products.json', 'w', encoding='utf-8') as f:
        json.dump(all_product_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main('https://www.ebay.com/b/Canon-Digital-SLR-Cameras/31388/bn_661')
