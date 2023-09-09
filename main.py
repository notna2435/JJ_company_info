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

#               -------GET COMPANY & AWARD NAMES FROM J&J WEBSITE-------
# Set up the web driver
service = Service('C:/Windows/chromedriver')
driver = webdriver.Chrome(service=service)
url = 'https://jnjinnovation.com/innovation-challenges/awardees'
driver.get(url)
time.sleep(20)
company_elements = driver.find_elements(By.CLASS_NAME, "tooltiptext")
element_list = []
name_and_award = [element_list.append(element.text.splitlines()) for element in company_elements]

# company_list = []
# award_list = []
# for element in element_list:
#     company_list.append(element[0])
#     if len(element) == 1:
#         award_list.append("None")
#     else:
#         award_list.append(element[1])
#
# clean_award_list = [award.replace("Awardee of ", "") for award in award_list]

time.sleep(2)
link_list = []
company_images = driver.find_elements(By.CLASS_NAME, "image")
for c in range(0, len(company_images)):
    if company_images[c].is_displayed():
        time.sleep(0.25)
        company_images[c].click()
        time.sleep(0.25)
        company_link = driver.find_element(By.LINK_TEXT, "Learn more")
        print(company_link.get_attribute("href"))
        link_list.append(company_link.get_attribute("href"))
        x_button = driver.find_element(By.CLASS_NAME, "xbutton")
        x_button.click()
        driver.execute_script("arguments[0].scrollIntoView();", company_images[c])

print(len(link_list))
print(link_list)


#                     -------RETRIEVE CONTACT INFO FROM COMPANY WEBSITE-------
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
}

# driver.get(link_text)
# time.sleep(5)
# contact_link = driver.find_element(By.LINK_TEXT, "Contact").get_attribute("href")
# print(contact_link)

driver.quit()  # DRIVER QUITS RIGHT HERE

# response = requests.get(
#     contact_link, headers=header)
#
# data = response.text
# soup = BeautifulSoup(data, "html.parser")
#
# email = soup.find("a", class_="lead")
# email_text = email.getText()
#
# address_and_phone = soup.find_all("span", class_="lead")
# address_and_phone_text = [text.getText().strip() for text in address_and_phone]
#
# modified_list = []
# for element in address_and_phone_text:
#     modified_element = element.replace('\n', ' ').strip()
#     modified_element = ' '.join(modified_element.split())
#     modified_list.append(modified_element)
#
# phone = modified_list[1]
# address = modified_list[0]

#                             -------PUT DATA IN DATABASE-------

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company-contacts.db'
# db = SQLAlchemy(app)
#
#
# class Companies(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company_name = db.Column(db.String(250), nullable=False, unique=True)
#     award = db.Column(db.String(250), nullable=False)
#     email = db.Column(db.String(250))
#     phone_number = db.Column(db.String(250))
#     address = db.Column(db.String(250))
#
#
# with app.app_context():
#     db.create_all()
#
#     for element in element_list:
#         if element[0] == "AgenT":
#             new_item = Companies(company_name=element[0], award=element[1].replace("Awardee of ", ""),
#                                  email=email_text, phone_number=phone, address=address)
#         elif len(element) == 1:
#             new_item = Companies(company_name=element[0], award="None")
#         else:
#             new_item = Companies(company_name=element[0], award=element[1].replace("Awardee of ", ""))
#         db.session.add(new_item)
#
#     db.session.commit()
