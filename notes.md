# Notes

### sqlite3
`.open <db name>`
`.tables` - view tables
`.schema <table name>` - view schema of table
SQL statements must end in `;`
`.q` - quit sqlite3



##### display data as cards using bootstrap

<div class="card-group">

  # loop through each seedling and create card
  <div class="card">
    <img class="card-img-top" src="..." alt="Card image cap">
    <div class="card-body">
      <h5 class="card-title">Card title</h5>
      <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
      <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
    </div>
  </div>

</div>


### pytests
test_create_connection
- normal connection
- incorrect file path
- path must be string

get_plant_id(id_name_dict, name_li)
- check if list of plant_id corresponds to name
- returns empty list if name_li not it id_name_dict

new_plant(known_seedlings, name_li)
- no new plant data known_seedlings.values == name_li

##### Thinking out loud
known_seedlings -> list containing seedling names that are in seedlings tables
name_li -> list of names scraped from website

new_plant_index = []
for name in name_li:
    if name not in known_seedlings:
        new_plant_index.append(name_li.index(name))

new_plant_index -> list containing index of new seedlings

if len(new_plant_index):
    new_seedlin_name_li = [name for name in name_li if name_li.index(name) in new_plant_index]
    # similar for description, price and img_url
    new_seedlings = True # flag
    <function to notify of new seedlings>

then insert new seedling_data into seedlings table <insert into table function>

then insert name and date into availability_dates table <a function>

---
c.execute("SELECT plant_id, name FROM seedlings")
rows = c.fetchall()
id_name_dict = dict(rows)
id_name_dict

name_id_dict = {v: k for k, v in id_name_dict.items()}
name_id_dict

plant_ids = []
for name in name_li:
    if name in name_id_dict:
        plant_ids.append(name_id_dict[name])
plant_ids

todays_date =  datetime.today().date()

plant_id_date = list(((d, str(todays_date)) for d in plant_ids))

c.executemany("INSERT INTO availability_dates (plant_id, available_date) \
               VALUES (?, ?)",
               plant_id_date)
print('updating availability_dates table')
conn.commit()
conn.close()


### Notification
#### Telegram
sending a message with Telegram accepts markdown, so can therefore embed picture of seedling with name.
as a picture will be more beneficial.
example:
``` python
bot_sendtext("""__The following seedlings are available:__
[Seedling Applegreen Eggplant R7.85](https://livingseeds.co.za/image-smp/seedling-applegreen-eggplantseedlings_10339_220x220.jpg)
""")
```
So I need to create template message to display seedling name, picture and price.
it seems the only one pic (the first) shows up, as telegram automatically shows a preview of the first link.
- so i can send a message for each seedling available
- create a table of img, name and price. figure out how to send message as markdown or maybe html
