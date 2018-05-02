#__auther__= 'Richard Chen Haoyu'
# coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Handler
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # see if the url ends with /hello
            if self.path.endswith("/hello"):
                # successful request
                self.send_response(200)
                # indicate the sending item is html
                self.send_header('Content-type', 'text/html')
                # end of the HTTP headers
                self.end_headers()

                # output text
                output = ""
                output += "<html><body>Hello!</body></html>"
                # show message
                self.wfile.write(output)
                # print for debugging
                print output
                return

            if self.path.endswith("/nihao"):
                self.send_response(200)
                # charset = utf-8 use Chinese in the html
                self.send_header('Content-type', 'text/html; charset="utf-8"')
                self.end_headers()

                output = ""
                output += "<html><body>你好! <a href = '/hello'>Back to Hello</a></body></html>"
                self.wfile.write(output)
                print output
                return
        except:
            self.send_error(404, "File Not Found %s" % self.path)
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