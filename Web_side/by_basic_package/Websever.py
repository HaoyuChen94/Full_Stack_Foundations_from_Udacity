#__auther__= 'Richard Chen Haoyu'
# coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# common gateway interface
import cgi

# Handler
class webserverHandler(BaseHTTPRequestHandler):
    # get from server
    # do_get, do_post override the method in BaseHTTPRequestHandler
    def do_GET(self):
        try:
            # see if the url ends with /hello
            if self.path.endswith("/hello"):
                # successful request
                self.send_response(200)
                # indicate the sending item is html
                self.send_header('content-type', 'text/html')
                # end of the HTTP headers
                self.end_headers()

                # output text
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                # show output
                self.wfile.write(output)
                # print for debugging
                print output
                return

            if self.path.endswith("/nihao"):
                self.send_response(200)
                # charset = utf-8 use Chinese in the html
                self.send_header('content-type', 'text/html; charset="utf-8"')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>你好!</h1> <a href = '/hello'>Back to Hello</a>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/nihao'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            # this line is for parse chinese correctly
            self.send_header('content-type', 'text/html; charset="utf-8"')
            self.end_headers()

            # get form
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # find the datatype of the form
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                # message: form name in the html code
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            # first in the message box
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass

# main
def main():
    try:
        # initiate the server
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