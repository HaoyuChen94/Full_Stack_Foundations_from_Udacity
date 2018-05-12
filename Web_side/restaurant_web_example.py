#__auther__= 'Richard Chen Haoyu'

# server package
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
# database package
from database_side.database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# setup the connection to the database
path = 'E:\\GitHub\\Full_Stack_Foundations_from_Udacity\\database_side'
engine = create_engine('sqlite:///' + path + '\\restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # query the restaurants
                restaurants = session.query(Restaurant).all()

                # output text
                output = ""
                output += "<html><body>"
                output += "<p><a href = '/restaurants/new'>Add a new Restaurant</a></p>"
                output += "<h1>Hello! Here is the restaurants: </h1>"
                output += "<p>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href = '/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a href = '/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</br></br>"
                output += "</p>"
                output += "</body></html>"

                # show output
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Add a new restaurant</h2>"
                output += "<p>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name= 'newRestaurantName' type='text' placeholder = 'New Restaurant Name'>"
                output += "<input type='submit' value='Create a new restaurant'></form>"
                output += "</p>"
                output += "</body></html>"

                # show output
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                # get the selected restaurant id from edit url
                restaurantIDPath = self.path.split("/")[2]
                # get the selected restaurant information
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>"
                    output += "You want to edit " + myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    # value -> default original input name
                    # placeholder -> show hint
                    output += "<input name = 'editRestaurantName' type='text' value = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                # show output
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                # get the selected restaurant id from edit url
                restaurantIDPath = self.path.split("/")[2]
                # get the selected restaurant information
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>"
                    output += "Are you sure you want to delete " + myRestaurantQuery.name + "?"
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                # show output
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # create new restaurant
                    newrestaurant = Restaurant(name=messagecontent[0])
                    session.add(newrestaurant)
                    session.commit()

                    # back to the main page
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('editRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    # if exist, do change
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                # if exist, do delete
                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "ctrl+C entered, stopping web server..."
        # close the server
        server.socket.close()

if __name__ == '__main__':
    main()