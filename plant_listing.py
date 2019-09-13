import re

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup


plants_dic = {}
name_li = []
descr_li = []
price_li = []

driver = webdriver.PhantomJS(executable_path='/Users/wahe3bru/Documents/phantomjs-2.1.1-macosx/bin/phantomjs')
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
            name_li.append(name)
            descr_li.append(description)
            price_li.append(price)
    next_page = bs.find('li', {'class':'active'}).next_sibling
    if next_page:
        driver.get(next_page.find(href=True)['href'])
        pageSource = driver.page_source
        bs = BeautifulSoup(pageSource, 'html.parser')
        print(next_page)

plants_dic['seedling'] = name_li
plants_dic['description'] = descr_li
plants_dic['price'] = price_li

seedling_df = pd.DataFrame.from_dict(plants_dic)
seedling_df['price'] = seedling_df.price.apply(lambda s: re.findall(r'^(R\d{1,2}\.\d\d)',s)[0])
seedling_df['description'] = seedling_df.description.str.replace('\\n\\n','').str.replace('Seedling','')
print(seedling_df)
