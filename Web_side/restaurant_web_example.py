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
                self.send_header('content-type', 'text/html')
                self.end_headers()

                # query the restaurants
                restaurants = session.query(Restaurant).all()

                # output text
                output = ""
                output += "<html><body>"
                output += "<h1>Hello! Here is the restaurants: </h1>"
                output += "<p>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br></br></br>"
                output += "</p>"
                output += "</body></html>"

                # show output
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

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