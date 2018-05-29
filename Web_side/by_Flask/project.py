#__auther__= 'Richard Chen Haoyu'

from flask import Flask, render_template
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_side.database_setup import Base, Restaurant, MenuItem

# setup the connection to the database
path = 'E:\\GitHub\\Full_Stack_Foundations_from_Udacity\\database_side'
engine = create_engine('sqlite:///' + path + '\\restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# if route ending with given name, run def
# '/' Give chance to lead the default url to the page, not 404
@app.route('/')
# route to specific restaurant
# final / to make the url available if the / is not there
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

    # Directly to output the html using string
    # output = ''
    # output += '<h1>Restaurant name: ' + restaurant.name + '</h1>'
    # output += '<h2>Menu: </h2>'
    # for i in items:
    #     output += i.name
    #     output += '</br>'
    #     output += i.price
    #     output += '</br>'
    #     output += i.description
    #     output += '</br>'
    #     output += '</br>'
    # return output

# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

# run this py only on the running py
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)