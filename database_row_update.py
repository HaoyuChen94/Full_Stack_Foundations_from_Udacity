#__auther__= 'Richard Chen Haoyu'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import Database and tables need to encounter
from database_setup import Base, Restaurant, MenuItem

### prepare the database and session
## indentify specific database
engine = create_engine('sqlite:///restaurantmenu.db')
## Bind engine to the Base
Base.metadata.bind = engine

## create session
# bind a session to the database
DBsession = sessionmaker(bind= engine)
# create the stage of manipulating Database
session = DBsession()

### update action
## search the item we want to change
# search in the menu of veggieburger
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

# feedback with sql query
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2)
print UrbanVeggieBurger
# feedback with selected object, add one when the result has just one object
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()
print UrbanVeggieBurger.price
# update the price for the UrbanVeggieBurger
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()
print UrbanVeggieBurger.price

# change all the veggieburger for the all the restaurant
for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"