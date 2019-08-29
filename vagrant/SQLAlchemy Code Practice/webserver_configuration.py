#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#Code above is necessary for all webserver program

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import BaseHTTPServer
import cgi #for POST request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem #import all table from 'table structure file'

engine = create_engine('sqlite:///restaurantmenu.db') #Connect your database file 
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Define the RequestHandlerclass here "webServerHandler"
class webserverHandler(BaseHTTPRequestHandler):
  
        def do_GET(self): #GET REQUEST
            try:
                '''....'''
                
            except:
   
        def do_POST(self): #POST REQUEST
            try:

                '''....'''
                '''....'''
            except:

    
#main function:
def main():
    try:
        #Class BaseHTTPServer.HTTPServer(server_address, RequestHandlerClass)
        port = 8080
        server = HTTPServer((" ", port), webserverHandler) #build Connection include port number and Handler class
        print("Web Server running on port %s" % port) #output port number on terminal
        server.server_forever() #serve_forever statement keep it listening until trigger "ctrl+C"
    
    except KeyboardInterrupt:
        print("^C entered, stopping web server") #type in ^C to stop the server.
        server.socket.close()

if __name__ == '__main__':
    main()
