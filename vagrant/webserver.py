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
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Define the RequestHandlerclass here "webServerHandler"
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self): #GET request
        #Which resources we are trying to access 
        try:
            #path is a variable support by BaseHTTPHandler
            #Contain URL sent by client to the server as string 
            if self.path.endswith('/hello'):
                self.send_response(200) #If recieve the URL from client end by '/hello', then response '200 OK'
                self.send_header('Content-type', 'text/html') #replying client by HTML type
                self.end_headers()

                #Create the reponse to the client 
                output = ""

                output += "<html><body>"
                output += "Hello!"
                #When client submit information show this
                output += '''<form method ='POST' enctype = 'multipart/form-data' action'/hello'><h2> 
                             What would you like me to say?
                             </h2><input name='message' type = 'text'><input type='submit' value='Submit'></form>'''
                output += "</body></html>"

                self.wfile.write(output.encode()) #wfile means write to the server, send it back to client
                print(output) #To see the string in terminal for debugging 
                return
            
            if self.path.endswith('/hola'):
                self.send_response(200) 
                self.send_header('Content-type', 'text/html') 
                self.end_headers()

                #Create a archor tag <a href= address>...</a>, it is a hyperlink, after href is the target address. 
                output = ""
                output += "<html><body>&#161Hola <a href = '/hello' >"
                output += "Back to Hello"
                output += '''<form method ='POST' enctype = 'multipart/form-data' action'/hello'><h2> 
                             What would you like me to say?
                             </h2><input name='message' type = 'text'><input type='submit' value='Submit'></form>'''
                output += "</a></body></html>"
                self.wfile.write(output.encode())  
                print(output)  
                return
            
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
                    output += "<a href='/restaurants/%s/edit'> Edit </a>" % restaurant.id #CRUD--Obj4--Give a "hyper link" to "Edit" option. 
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
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value ='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output.encode())
                return
        
        #CRUD---Obj4---Click "Edit" and jump to a new Edit webpage
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
            
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    output = ""
                    output += "<html><body><h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form></body></html>"

                    self.wfile.write(output)
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

                #CRUD---obj3---CRUD, 'Create' functionality
                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301) #send 301 to client that indicate success receive post request
                self.send_header('Content-type',  'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            
            #CRUD---Obj4---User input to change the name of restaurant
                if self.path.endswith('/edit'):
                  ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                  if ctype == 'multipart/form-data': 
                    fields = cgi.parse_multipart(self.rfile, pdict) 
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRetaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301) #send 301 to client that indicate success receive post request
                        self.send_header('Content-type',  'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            '''#CRUD---Obj1---output to webpage what user input
            #Extract the information that submit by client 
            #cgi.parse_header function parse HTML form from header, like content type
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data': #if we received form data, then ...
                fields = cgi.parse_multipart(self.rfile, pdict) #Collect all of the fields in a form
                messagecontent = fields.get('message') #get value of a sepcific field and store them in an array
            
            #Tell client what information we received
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0] #show out the received information to client 

            #To prompt user to input data, the input field as 'message', coincide to the 'message' which extract data in POST request
            output += "<form method ='POST' enctype = 'multipart/form-data' action'/hello'><h2> 
            What would you like me to say?
            </h2><input name='message' type = 'text'><input type='submit' value='Submit'></form>"
            output += "</body></html>"

            self.wfile.write(output)
            print(output)'''

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


