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
                    output += "<a href = '#'>Edit</a>"
                    output += "</br>"
                    output += "<a href = '#'>Delete</a>"
                    output += "</br>"
                output += "</p>"
                output += "</body></html>"

                # show output
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # output text
                output = ""
                output += "<html><body>"
                output += "<h2>Add a new restaurant</h2>"
                output += "<p>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newRestaurantName" type="text" placeholder = "New Restaurant Name">
                <input type="submit" value="Create a new restaurant"></form>'''
                output += "</p>"
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