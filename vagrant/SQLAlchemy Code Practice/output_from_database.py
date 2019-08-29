
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #for POST request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem #import all table from 'table structure file'

engine = create_engine('sqlite:///restaurantmenu.db') #Connect your database file 
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
            
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"

                output += "</html></body>"

                self.wfile.write(output.encode())
                print(output)
                return
        except:
            self.send_error(404, 'File Not Found %s' % self.path)



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("The Website port number is %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server")
        server.socket.close()

if __name__ == '__main__':
    main()
