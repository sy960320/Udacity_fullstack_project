#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import BaseHTTPServer
import cgi #for POST request

#CRUD---We already set up the restaurant database in the previous lesson, so we can direct quote it
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem 
#CRUD---Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Define the RequestHandlerclass here "webServerHandler"
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self): #GET request
        #Which resources we are trying to access 
        try:
        #CRUD---obj1---list all restarant name from datbase on webpage 
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                self.send_response(200) 
                self.send_header('Content-type', 'text/html') 
                self.end_headers()

                output = ""
                output += "<html><body>"
                #CRUD---obj3---Make a new Restaurant hyperlink 
                output += "<a href = '/restaurants/new'> Make a new Restaurant Here </a></br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    #CRUD---Obj2---Create a link to edit and delete each restaurant
                    output += "<a href = '#'> Edit </a>"
                    output += "</br>" #means 'enter'
                    output += "<a href = '#'> Delete </a>"
                    output += "</br></br></br>"
                output += "</body></html>"

                self.wfile.write(output.encode())
                print(output)
                return 

        #CRUD---Obj3---Create a link named 'Make a new Restaurant' with localhost:8080/restaurants/new
        #Use this link combine with POST_REQUEST funtionality to create a new restaurant in database 
            if self.path.endswith("/restaurants/new"):  
                self.send_response(200) 
                self.send_header('Content-type', 'text/html') 
                self.end_headers()

                output = " "
                output += "<html><body>"
                output += "<h1>Make a new Restaurant</h1>"
                output += "<form method ='POST' enctype = 'multipart/form-data' action = '/restaurants/new'>"
                output += "<input name ='newRestaurantName' type = 'text' placeholder = 'New Restaurant Name'>"
                output += "<input type ='submit' value ='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output.encode())
                return


        except IOError: #Can not find the URL
            self.send_error(404, 'File Not Found %s' % self.path)
    
    def do_POST(self):
        try:
            #CRUD---Obj3---submit the new restaurant in database
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data': 
                    fields = cgi.parse_multipart(self.rfile, pdict) 
                    messagecontent = fields.get('newRestaurantName')
                #CRUD---obj3---CRUD, create functionality
                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

            self.send_response(301) #send 301 to client that indicate success receive post request
            self.send_header('Content-type', 'text/html')
            self.send_header('Location','/restaurants')
            self.end_headers()
        except:
            pass



#The main method, inside main()
def main():
    try:
        #Create HTTPServerClass， HTTPServer build off of a TCPServer
        #Class BaseHTTPServer.HTTPServer(server_address, RequestHandlerClass)
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print("Web Server running on port %s" % port) #know my server is running
        server.serve_forever() #serve_forever statement keep it listening until trigger ctrl+C

    #Exception triggered when user hold ctrl + C on the keyboard 
    #When Exception occured, stop the server  
    except KeyboardInterrupt:
        print("^C entered, stopping web server") #type in ^C to stop the server. 
        server.socket.close()
    

#Execute the main() method
if __name__ == '__main__':
    main()


