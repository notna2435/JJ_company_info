from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from selenium.webdriver.common.keys import Keys
import time
import os

SAMPLE_LIST = ['AgenT', 'Acclinate', 'AmacaThera', 'Atro Medical', 'biotx.ai', 'Grapheal', 'MabSwitch, Inc',
               'siRNAgen Therapeutics', 'Vaxess Technologies']

# Set up the web driver
service = Service('C:/Windows/chromedriver')
driver = webdriver.Chrome(service=service)
url = 'https://jnjinnovation.com/innovation-challenges/awardees'
driver.get(url)
time.sleep(15)
company_elements = driver.find_elements(By.CLASS_NAME, 'tooltiptext')
element_list = []
name_and_award = [element_list.append(element.text.splitlines()) for element in company_elements]
sample_elements = []
for x in element_list:
    for company in SAMPLE_LIST:
        if company == x[0]:
            sample_elements.append(x)
# print(sample_elements)

time.sleep(2)
sample_link_list = []
company_images = driver.find_elements(By.CLASS_NAME, 'image')
for c in range(0, len(company_images)):
    if company_images[c].is_displayed():
        time.sleep(0.25)
        company_images[c].click()
        time.sleep(0.25)
        heading = driver.find_element(By.CLASS_NAME, 'descriptioncontent').text.splitlines()
        if heading[0] in SAMPLE_LIST:
            company_link = driver.find_element(By.LINK_TEXT, 'Learn more')
            print(company_link.get_attribute('href'))
            sample_link_list.append(company_link.get_attribute('href'))
        x_button = driver.find_element(By.CLASS_NAME, 'xbutton')
        x_button.click()
        driver.execute_script('arguments[0].scrollIntoView();', company_images[c])


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
}

email_list = []
phone_list = []
address_list = []

# AgenT Contact Info
driver.get(sample_link_list[0])
time.sleep(5)
agent_contact = driver.find_element(By.LINK_TEXT, 'Contact').get_attribute('href')

response_1 = requests.get(
    agent_contact, headers=header)

agent_data = response_1.text
soup = BeautifulSoup(agent_data, 'html.parser')

email = soup.find('a', class_='lead')
agent_email = email.getText()

address_and_phone = soup.find_all('span', class_='lead')
address_and_phone_text = [text.getText().strip() for text in address_and_phone]

modified_list = []
for element in address_and_phone_text:
    modified_element = element.replace('\n', ' ').strip()
    modified_element = ' '.join(modified_element.split())
    modified_list.append(modified_element)

agent_phone = modified_list[1]
agent_address = modified_list[0]

email_list.append(agent_email)
phone_list.append(agent_phone)
address_list.append(agent_address)

# Acclinate Contact Info
driver.get(sample_link_list[1])
time.sleep(2)
acclinate_contact = driver.find_element(By.LINK_TEXT, 'Contact').get_attribute('href')

response_2 = requests.get(
    acclinate_contact, headers=header)

data = response_2.text
soup = BeautifulSoup(data, 'html.parser')

acclinate_email_phone = str(soup.find('p', class_='paragraph-49')).replace('<br/>', '\n').splitlines()
acclinate_phone = acclinate_email_phone[2]
acclinate_email = acclinate_email_phone[3]
acclinate_address_element = str(soup.find('p', class_='paragraph-48')).replace('<br/>', '\n').splitlines()
acclinate_address = acclinate_address_element[4].replace('</strong>', '') + ', ' + acclinate_address_element[5].replace('</p>', '')

email_list.append(acclinate_email)
phone_list.append(acclinate_phone)
address_list.append(acclinate_address)

#AmacaThera Contact Info
response_3 = requests.get(
    sample_link_list[2], headers=header)

data = response_3.text
soup = BeautifulSoup(data, 'html.parser')

amacathera_contact_info = soup.find('div', class_='contact').text.splitlines()
amacathera_phone = amacathera_contact_info[1]
amacathera_address = amacathera_contact_info[2] + ' ' + amacathera_contact_info[3].replace('\xa0', ' ') + ' ' + amacathera_contact_info[4].replace('inf[email\xa0protected]', '')
amacathera_email = 'info@amacathera.ca'

email_list.append(amacathera_email)
phone_list.append(amacathera_phone)
address_list.append(amacathera_address)

# Atro Medical Contact Info
driver.get(sample_link_list[3])
time.sleep(2)
atro_medical_contact = driver.find_element(By.LINK_TEXT, 'Contact').get_attribute('href')

response_4 = requests.get(
    atro_medical_contact, headers=header)

data = response_4.text
soup = BeautifulSoup(data, 'html.parser')

atro_medical_info = soup.find('p', class_='sc-jSMfEi inoWfC')
atro_medical_email = str(atro_medical_info.find('a')).split('"')[1].replace('mailto:', '')
split_atro_medical_info = str(atro_medical_info).replace('<br/>', '\n').splitlines()
atro_medical_address = split_atro_medical_info[1].replace('<!-- -->', ', ') + split_atro_medical_info[2].replace('<!-- -->', '')
atro_medical_phone = 'None'

email_list.append(atro_medical_email)
phone_list.append(atro_medical_phone)
address_list.append(atro_medical_address)

#biotx.ai Contact Info
response_5 = requests.get(
    sample_link_list[4], headers=header)

data = response_5.text
soup = BeautifulSoup(data, 'html.parser')

biotx_email_phone = str(soup.find('div', class_='undefined').find_all('li', class_='nav-item')).replace('<!-- -->', '\n').splitlines()
biotx_email = biotx_email_phone[7].strip()
biotx_phone = biotx_email_phone[3].strip()
biotx_address_element = str(soup.find('div', class_='undefined').find_all('p')).replace('<p>', '\n').splitlines()
biotx_address = biotx_address_element[3].replace('</p>]', '')

email_list.append(biotx_email)
phone_list.append(biotx_phone)
address_list.append(biotx_address)

# Grapheal Contact Info
driver.get(sample_link_list[5])
time.sleep(2)
grapheal_contact = driver.find_element(By.XPATH, '//*[@id="comp-igauz7ee6"]/a').get_attribute('href')

driver.get(grapheal_contact)
grapheal_address_row1 = driver.find_element(By.XPATH, '//*[@id="comp-kvs16ime"]/p[1]/span/span/span/span').text
grapheal_address_row2 = driver.find_element(By.XPATH, '//*[@id="comp-kvs16ime"]/p[2]/span/span/span/span').text
grapheal_address_row3 = driver.find_element(By.XPATH, '//*[@id="comp-kvs16ime"]/p[3]/span/span/span/span').text
grapheal_address = grapheal_address_row1 + ' ' + grapheal_address_row2 + ', ' + grapheal_address_row3.strip()
grapheal_phone_1 = driver.find_element(By.XPATH, '//*[@id="comp-kvs16ime"]/p[6]/span/span/span/span').text
grapheal_phone_2 = driver.find_element(By.XPATH, '//*[@id="comp-kvs16ime"]/p[7]/span/span/span/span/span').text
grapheal_phone = grapheal_phone_1.replace('Tel: ', '') + ', ' + grapheal_phone_2.replace('Tel: ', '')

response_6 = requests.get(
    grapheal_contact, headers=header)

data = response_6.text
soup = BeautifulSoup(data, 'html.parser')

grapheal_contact_info = soup.find('div', id='comp-kvs16ime')
grapheal_email = grapheal_contact_info.find('a').get_text()

email_list.append(grapheal_email)
phone_list.append(grapheal_phone)
address_list.append(grapheal_address)

# MabSwitch Contact Info
driver.get(sample_link_list[6])
time.sleep(2)
mabswitch_email_element = driver.find_element(By.XPATH, '//*[@id="contact"]/div/div/div[1]/div/div[2]/div[2]').text
mabswitch_email = mabswitch_email_element.replace(' (at) ', '@').replace('Email Us\n', '')
mabswitch_phone = 'None'
mabswitch_address = 'None'

email_list.append(mabswitch_email)
phone_list.append(mabswitch_phone)
address_list.append(mabswitch_address)

# siRNAgen Contact Info
response_8 = requests.get(
    sample_link_list[7], headers=header)

data = response_8.text
soup = BeautifulSoup(data, 'html.parser')

sirnagen_email = str(soup.find_all('a', class_='wixui-rich-text__text')[1]['href']).replace('mailto:', '')
sirnagen_phone = 'None'
sirnagen_address = 'None'

email_list.append(sirnagen_email)
phone_list.append(sirnagen_phone)
address_list.append(sirnagen_address)

#Vaxess Contact Info
driver.get(sample_link_list[8])
time.sleep(2)
vaxess_address = driver.find_element(By.XPATH, '//*[@id="block-13d4d317044cfd51f303"]/div/div/p[1]').text
vaxess_email = driver.find_element(By.XPATH, '//*[@id="block-13d4d317044cfd51f303"]/div/div/p[4]').text
vaxess_phone = 'None'

email_list.append(vaxess_email)
phone_list.append(vaxess_phone)
address_list.append(vaxess_address)

driver.quit()  # DRIVER QUITS RIGHT HERE

#                             -------PUT DATA IN DATABASE-------

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company-contacts.db'
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'sample-company-contacts.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'sample_python'
db = SQLAlchemy(app)


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False, unique=True)
    award = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250))
    phone_number = db.Column(db.String(250))
    address = db.Column(db.String(250))


with app.app_context():
    db.create_all()

    for i in range(0, len(sample_elements)):
        if len(sample_elements[i]) == 1:
            new_item = Sample(company_name=sample_elements[i][0], award="None", link=sample_link_list[i],
                              email=email_list[i], phone_number=phone_list[i], address=address_list[i])
        else:
            new_item = Sample(company_name=sample_elements[i][0], award=sample_elements[i][1].replace("Awardee of ", ""),
                              link=sample_link_list[i], email=email_list[i], phone_number=phone_list[i], address=address_list[i])
        db.session.add(new_item)

    db.session.commit()
