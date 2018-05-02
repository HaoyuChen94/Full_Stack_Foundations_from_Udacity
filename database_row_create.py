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

## insert action
# create one row
newrestaurant = Restaurant(name = "Pizza Hut")
# put it to the to-do list
session.add(newrestaurant)
# commit the change
session.commit()

# menu item insert action
newitem = MenuItem(name="Nice Pizza", description="Nice Pizza in Pizza Hut", course="Entree", price="$10.00", restaurant= newrestaurant)

session.add(newitem)
session.commit()
