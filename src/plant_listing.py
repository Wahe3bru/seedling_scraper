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

# old way deprecated
# driver = webdriver.PhantomJS(executable_path=r'C:\Users\WaheebA\Documents\work\learnings\webscraping\webscraping_book\phantomjs-2.1.1-windows\bin\phantomjs')
#driver = webdriver.PhantomJS(executable_path='/Users/wahe3bru/Documents/phantomjs-2.1.1-macosx/bin/phantomjs')

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
        print(next_page)

plants_dic['seedling'] = name_li
plants_dic['description'] = descr_li
plants_dic['price'] = price_li
plants_dic['pic_url'] = pic_li

seedling_df = pd.DataFrame.from_dict(plants_dic)
seedling_df['price'] = seedling_df.price.apply(lambda s: re.findall(r'^(R\d{1,2}\.\d{2})',s)[0])
seedling_df['description'] = seedling_df.description.str.replace('\\n{1,2}','').str.replace('Seedling','')
print(seedling_df)
