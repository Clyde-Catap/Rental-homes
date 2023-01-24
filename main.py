import requests
import re
from bs4 import BeautifulSoup
from  selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os


DOCS_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSexdhXFnpOtnfVKXCMYUcW56zFgj_dK880pf3MEZxdL3EtGnw/viewform?usp=sf_link'

RENTAL_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'

ADDITION = 'https://www.zillow.com'


headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "en-PH,en-US;q=0.9,en;q=0.8"
}


response = requests.get(RENTAL_URL, headers=headers)
data = response.content



soup = BeautifulSoup(data, 'lxml')
data_houses = soup.find_all( 'li', class_="ListItem-c11n-8-81-1__sc-10e22w8-0 srp__hpnp3q-0 enEXBq with_constellation")
price = soup.find_all(class_='StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0 wgiFT')
add = soup.find_all('a', class_="StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0 lpqUkW property-card-link")


final_data = data_houses[:7]

prices = []
address = []
link = []

new_list = []

for pr in price:
    x = pr.text
    prices.append(x)
for ad in add:
    w = ad.text
    address.append(w)
for ln in add:
    q = ln['href']
    link.append(q)

for r in link:
    if r[0] != "h":
        qew = ADDITION + r
        link[link.index(r)] = qew



print(prices)
print(address)
print(link)
#
for prop in address:

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    s = Service("P:\Chrome Driver\chromedriver.exe")

    driver = webdriver.Chrome(options=chrome_options, service=s)
    driver.maximize_window()
    driver.get(DOCS_URL)

    time.sleep(3)
    prop_address_entry = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prop_address_entry.send_keys(prop)

    prop_prices_entry = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prop_prices_entry.send_keys(prices[address.index(prop)])

    prop_link_entry = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prop_link_entry.send_keys(link[address.index(prop)])

    time.sleep(2)
    submit_button  = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit_button.click()


    time.sleep(5)

    driver.quit()


