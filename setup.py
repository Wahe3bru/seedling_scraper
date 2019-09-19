from pathlib import Path
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    '''create connection to slqite database
    param
       db_file - path to sqlite database
    return
        conn - connection object or None
    '''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# save this to env file
database = Path.cwd() / 'data' / 'seedlings.db'
# Create db
conn = create_connection(str(database))
c = conn.cursor()

# Create seedlings table
create_seedlings_table = """
CREATE TABLE IF NOT EXISTS seedlings(
    plant_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price text,
    img_url TEXT
);"""
c.execute(create_seedlings_table)
print('created seedlings table')

# Create availability table
create_availability_date = """
CREATE TABLE IF NOT EXISTS availability_dates(
    plant_id INTEGER NOT NULL,
    available_date TEXT NOT NULL,
    FOREIGN KEY (plant_id) REFERENCES seedlings (plant_id)
);"""
c.execute(create_availability_date)
print('created availability_dates table')

# scrape website
print('scraping data...')
import re
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


plants_dic = {}
name_li = []
descr_li = []
price_li = []
pic_li = []

todays_date =  datetime.today().date()
# windows
chrome_driver_path = Path('C:/Users/WaheebA/Documents/work/learnings/webscraping/chromedriver.exe')
# mac
# chrome_driver_path = Path()

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
driver = webdriver.Chrome(executable_path=str(chrome_driver_path), options=chrome_options)

driver.get('https://livingseeds.co.za/heirloom-seedlings')

pageSource = driver.page_source
bs = BeautifulSoup(pageSource, 'html.parser')

next_page = 1
while next_page:
    plant_list = bs.find_all('div', {'class': 'caption'})
    if plant_list:
        for plant in plant_list:
            name = plant.h4.get_text()
            description = plant.p.get_text()
            price = plant.find('p',{'class': 'price'}).get_text().strip()
            plant_pic = plant.parent.parent.find('div', {'class': 'image'}).find(src=True)['src']

            name_li.append(name)
            descr_li.append(description)
            price_li.append(price)
            pic_li.append(plant_pic)

    next_page = bs.find('li', {'class':'active'}).next_sibling
    if next_page:
        driver.get(next_page.find(href=True)['href'])
        pageSource = driver.page_source
        bs = BeautifulSoup(pageSource, 'html.parser')

# plants_dic['seedling'] = name_li
# plants_dic['description'] = descr_li
# plants_dic['price'] = price_li
# plants_dic['pic_url'] = pic_li

# clean description
descr_li_clean = [ d.replace('Seedling', '').replace('\n', '') for d in descr_li] # .replace('\\n{1,2}', '')
# extract price
sale_price = [re.findall(r'^(R\d{1,2}\.\d{2})', price)[0] for price in price_li]
# populate table
# insert into seedlings table
print('updating seedlings table')
for i in range(len(name_li)):
    c.execute("INSERT INTO seedlings (name, description, price, img_url) VALUES (?, ?, ?, ?)",
             (name_li[i], descr_li_clean[i], sale_price[i], pic_li[i]))
# get data ready for  table insert format
c.execute("SELECT plant_id, name FROM seedlings")
rows = c.fetchall()
id_name_dict = dict(rows)
plant_id_date = list(((d, str(todays_date)) for d in list(id_name_dict.keys())))
# insert into availability_dates tables
c.executemany("INSERT INTO availability_dates (plant_id, available_date) VALUES (?, ?)",
          plant_id_date)
print('updating availability_dates table')
conn.commit()
conn.close()
