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

### delete action
## search the item want to delete
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print spinach.restaurant.name
# delete item
session.delete(spinach)
session.commit()
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
