from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from selenium.webdriver.common.keys import Keys
import time

service = Service('C:/Windows/chromedriver')
driver = webdriver.Chrome(service=service)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
}

sample_link_list = ["https://www.agent-biotech.com/", "https://www.acclinate.com/", "https://www.amacathera.ca/",
                    "https://dev.atromedical.com/", "https://www.biotx.ai/", "https://www.grapheal.com/", "https://mabswitch.com/",
                    "https://www.sirnagen.com/", "https://www.vaxess.com/"]

# driver.get(sample_link_list[6])
# time.sleep(2)
response_5 = requests.get(
    sample_link_list[4], headers=header)

data = response_5.text
soup = BeautifulSoup(data, 'html.parser')

biotx_email_phone = str(soup.find('div', class_='undefined').find_all('li', class_='nav-item')).replace('<!-- -->', '\n').splitlines()
biotx_email = biotx_email_phone[7].strip()
print(biotx_email)
biotx_phone = biotx_email_phone[3].strip()
biotx_address_element = str(soup.find('div', class_='undefined').find_all('p')).replace('<p>', '\n').splitlines()
biotx_address = biotx_address_element[3].replace('</p>]', '')


# vaxess_contact = driver.find_element(By.XPATH, '//*[@id="comp-igauz7ee6"]/a').get_attribute('href')
# print(grapheal_contact)
#
# response_8 = requests.get(
#     sample_link_list[7], headers=header)
#
# data = response_8.text
# soup = BeautifulSoup(data, 'html.parser')


