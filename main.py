from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import argparse


parser = argparse.ArgumentParser(description="Image Downloader")

parser.add_argument("-s", type=str, help="Search")
parser.add_argument("-t", type=int, help="Total")

args = parser.parse_args()
search_for = args.s if args.s else 'garden'
total = args.t if args.t else 30

driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))
URL = 'https://unsplash.com/'
driver.get(URL)


# Searching the keywords
search = driver.find_element(
    By.XPATH, '//input[@data-testid="nav-bar-search-form-input"]')
search.send_keys(search_for)
search.send_keys(Keys.RETURN)


# Scrolling for more images

height = 0
image_tags = []
i = 1

while True:
    i += 1
    print(f"Loop no. {i+1}")
    height = height + 1000
    driver.execute_script(f"window.scrollTo(0,{height});")
    time.sleep(1)
    try:
        load_more = driver.find_element(
            By.XPATH, "//button[text()='Load more']")
        load_more.click()
    except:
        print("No 'Load more' button found.")
    image_tags = driver.find_elements(
        By.XPATH, "//img[@itemprop='thumbnailUrl']")
    print(len(image_tags))

    if len(image_tags) >= total:
        break


# Getting image URLS

image_tags = driver.find_elements(
    By.XPATH, "//img[@itemprop='thumbnailUrl']")
img_urls = [img.get_attribute(
    'src') for img in image_tags if 'images' in img.get_attribute('src')]


# Downloading Images

for index, url in enumerate(img_urls[:total]):
    response = requests.get(url, stream=True)
    with open(f'img-{index+1}.jpg', 'wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)
driver.close()
