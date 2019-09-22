import re
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

import db_helper as db


name_li = []
descr_li = []
price_li = []
pic_li = []

# windows
chrome_driver_path = Path('C:/Users/WaheebA/Documents/work/learnings/webscraping/chromedriver.exe')
# mac
# chrome_driver_path = Path()

url = 'https://livingseeds.co.za/heirloom-seedlings'


def connect_and_get_source(url, chrome_driver_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(executable_path=str(chrome_driver_path),
                              options=chrome_options)

    driver.get(url)
    return driver.page_source


pageSource = connect_and_get_source(url, chrome_driver_path)
bs = BeautifulSoup(pageSource, 'html.parser')

next_page = 1
while next_page:
    plant_list = bs.find_all('div', {'class': 'caption'})
    if plant_list:
        for plant in plant_list:
            name = plant.h4.get_text()
            description = plant.p.get_text()
            price = plant.find('p', {'class': 'price'}).get_text().strip()
            plant_pic = plant.parent.parent.find('div', {'class': 'image'}
                                                ).find(src=True)['src']

            name_li.append(name)
            descr_li.append(description)
            price_li.append(price)
            pic_li.append(plant_pic)

    next_page = bs.find('li', {'class': 'active'}).next_sibling
    if next_page:
        # driver.get(next_page.find(href=True)['href'])
        next_url = next_page.find(href=True)['href']
        # pageSource = driver.page_source
        pageSource = connect_and_get_source(next_url, chrome_driver_path)
        bs = BeautifulSoup(pageSource, 'html.parser')
        print(next_page)

# clean description
descr_li = [d.replace('Seedling', '').replace('\n', '') for d in descr_li]
# extract price
price_li = [re.findall(r'^(R\d{1,2}\.\d{2})', price)[0] for price in price_li]

# end webscraping

# update db
db_file = database = Path.cwd() / 'data' / 'seedlings.db'

conn = db.create_connection(db_file)
c = conn.cursor()
id_name_dict = db.id_names_from_db(conn)


def get_plant_id(id_name_dict, name_li):
    """Get the plant_id from db.seedlings.
    params:
        id_name_dict: dict. seedling_id and seedling names from db.seedlings
        name_li: list. seedling names scraped from website
    return:
        new_plant_index: list of index for new seedlings
    """
    name_id_dict = {v: k for k, v in id_name_dict.items()}

    plant_idx = []
    for name in name_li:
        if name in name_id_dict:
            plant_idx.append(name_id_dict[name])
    return plant_idx


def new_plant(known_seedlings, name_li):
    """Append index to list if seedling name not in known_seedlings.
    Args
        known_seedlings (list): plant_id, name tuple from db.seedlings
        name_li (list): names of seedlings scraped
    Returns
        new_plant_index (list)
    """
    new_plant_index = []
    for name in name_li:
        if name not in known_seedlings.values:
            new_plant_index.append(name_li.index(name))
    return new_plant_index


new_plants_idx = new_plant(id_name_dict, name_li)
if new_plants_idx:
    new_name_li = [name for name in name_li
                   if name_li.index(name) in new_plants_idx]
    new_description = [desc for desc in descr_li
                       if descr_li.index(desc) in new_plants_idx]
    new_price = [price for price in price_li
                 if price_li.incex(price) in new_plants_idx]
    new_img_url = [img for img in pic_li if pic_li.index(img) in new_plants_idx]
    new_seedlings = True  # flag
    # <function to notify of new seedlings>

    # insert new seedlings into db.seedlings
    db.update_seedlings_table(conn, new_name_li, new_description, new_price,
                           new_img_url)

plant_index = get_plant_id(id_name_dict, name_li)
# insert into db.availabilty_dates table
db.update_availability_dates_table(conn, plant_index)
