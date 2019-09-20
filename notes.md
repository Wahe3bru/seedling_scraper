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
