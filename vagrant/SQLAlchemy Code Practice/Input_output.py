#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import BaseHTTPServer
import cgi #for POST request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem 

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#GOAL: List all restaurant name from database on localhost:8080/restaurants
class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.send.path.endswith("/restaurants"):
                #after user sucess connect the server, we response this to user
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
             
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                for r in restaurants:
                    output += r.name
                    output += "</br>"

                output += "</body></html>"
                self.wfile.write(output.encode())
                return
        except IOError: #Can not find the file
            self.send_error(404, 'File Not Found %s' % self.path)






#main function:
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    
    except KeyboardInterrupt:
        print("^C entered, stopping web server")
        server.socket.close()

if __name__ == '__main__':
    main()
