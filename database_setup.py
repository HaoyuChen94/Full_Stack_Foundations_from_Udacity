#__auther__= 'Richard Chen Haoyu'

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

## start configuration
# initiate a database class (declaraticve base)
Base = declarative_base()

## build tables classes
# create tables class (in Base class)
class Restaurant(Base):
    # indicate name of table
    __tablename__ = 'restaurant'

    # mapper information(columns in the table)
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    # related to the restaurant database
    restaurant = relationship(Restaurant)

## end of configuration
# create a specific database
engine = create_engine('sqlite:///restaurantmenu.db')

# add table class to the database
Base.metadata.create_all(engine)