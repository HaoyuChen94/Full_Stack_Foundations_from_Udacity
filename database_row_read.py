#__auther__= 'Richard Chen Haoyu'

# try this after running the lotsofmenus.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import Database and tables need to encounter
from database_setup import Base, Restaurant, MenuItem

## indentify specific database
engine = create_engine('sqlite:///restaurantmenu.db')
## Bind engine to the Base
Base.metadata.bind = engine

## create session
# bind a session to the database
DBsession = sessionmaker(bind= engine)
# create the stage of manipulating Database
session = DBsession()

## read action
# query the first item
firstresult = session.query(Restaurant).first()
print firstresult.name
# query all the items
results = session.query(Restaurant).all()
for result in results:
    print result.id, ": ", result.name