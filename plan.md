
seedlings table -> seedling_id, name, desc, price, img_url
available_dates table -> id, seedling_id, date

get (seedling_id, name) from seedlings table  
    -> turn to dict {seedling_id: name} -> stored_seedlings_map

```python
while next_page:
    plant_list = bs.find_all('div', {'class': 'caption'})
    if plant_list:
        for plant in plant_list:
            name = plant.h4.get_text()
            if name not in stored_seedlings_map.values:
                description = plant.p.get_text()
                price = plant.find('p',{'class': 'price'}).get_text().strip()
                plant_pic = plant.parent.parent.find('div', {'class': 'image'}).find(src=True)['src']

                name_li.append(name)
                descr_li.append(description)
                price_li.append(price)
                pic_li.append(plant_pic)
            else:
              add_date_to_id_li.append(name)
```
clean webscraped data

add new seedling data to seedlings table

get (seedling_id, name) from seedlings table  
    -> turn to dict {seedling_id: name} -> stored_seedlings_map

get insert data into correct format -> (seedling_id, date) from stored_seedlings_map

insert data to available_dates table
