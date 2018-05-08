#__auther__= 'Richard Chen Haoyu'

# try this after running the lotsofmenus.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import Database and tables need to encounter
from database_setup import Base, Restaurant, MenuItem
import os

### prepare the database and session
## indentify specific database
# get project path
path = os.getcwd()
path = 'E:\\GitHub\\Full_Stack_Foundations_from_Udacity\\database_side'
engine = create_engine('sqlite:///' + path + '\\restaurantmenu.db')
## Bind engine to the Base
Base.metadata.bind = engine

## create session
# bind a session to the database
DBsession = sessionmaker(bind= engine)
# create the stage of manipulating Database
session = DBsession()

### read action
# query the first item
firstresult = session.query(Restaurant).first()
print firstresult.name
# query all the items
results = session.query(Restaurant).all()
for result in results:
    print result.id, ": ", result.name
