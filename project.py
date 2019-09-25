from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#q1:Show name, price and description from a sepecific restaurant by Flask 
#q2: Routing 
#q3: Template
#q4: URL Building
#q5: Request and Redirect 

@app.route('/')
#q2
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    #q3
    return render_template('menu.html',restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET', 'POST']) #This webpage can do Request
def newMenuItem(restaurant_id):
    if request.method == 'POST': #gather the method if it is 'POST' reuqest
         #'Create' function of CRUD, gather the data that input in web, the variable of data is 'name'
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit() #commit the change 
        #After finish it, redirect the webpage to main page
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        #If web server recieve 'GET' request, then stay on the same webpage
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    updateItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            updateItem.name = request.form['name']

        session.add(updateItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id=menu_id)
        #return render_template('menu.html',restaurant = restaurant, items = items)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)