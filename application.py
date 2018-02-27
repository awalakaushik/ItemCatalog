#!/usr/bin/python

from flask import Flask
from flask import render_template, request, redirect
from flask import url_for, flash, jsonify

# CRUD functionality
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, Category, CategoryItem, User

# Imports for OAuth implementation
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read()
    )['web']['client_id']
APPLICATION_NAME = "Sports Catalog Application"

engine = create_engine('sqlite:///itemcatalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" %login_session['state']
    return render_template('login.html', STATE=state)

# Route for gconnect OAuth implementation


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        console.log("Token accepted!")
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style="width: 300px; height: 300px;\
    border-radius: 150px;-webkit-border-radius: 150px;\
    -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Function

# get user id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# get user information
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Creating the a new user
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
@app.route('/logout')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'%(login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # return response
        return redirect('/catalog/')
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Making an API endpoint (GET Request)
@app.route('/catalog/category_items.json')
def catalogListJSON():
    items = session.query(CategoryItem).all()
    return jsonify(CatalogItems=[item.serialize for item in items])


@app.route('/catalog/<string:category_name>.json')
def catalogIdJSON(category_name):
    cat = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(category_id=cat.id).all()
    return jsonify(category_name=[item.serialize for item in items])


@app.route('/catalog/category.json')
def catalogCategoryJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[category.serialize for category in categories])


# Route to display the categories of an item catalog at the root
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    """ Displays catalog list and the latest added items on the
    home page of the application. """
    categories = session.query(Category).all()

    # Fetch the totals of the items and send the list to homw.html
    itemTotals = {}
    output = ""
    for category in categories:
        itemTotal = session.query(CategoryItem).filter_by(category_id=category.id).count()
        itemTotals[category] = itemTotal
    # render the template
    if 'username' not in login_session:
        return render_template(
            'publichome.html',
            categories=categories,
            itemTotals=itemTotals)
    else:
        return render_template(
            'home.html',
            categories=categories,
            itemTotals=itemTotals)


# Route to display items of a specific category
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showCategoryItemList(category_name):
    """ Displays items for a selected category """
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    itemTotal = session.query(CategoryItem).filter_by(category_id=category.id).count()

    # render the template
    return render_template(
        'items.html',
        categories=categories,
        category=category,
        items=items,
        itemTotal=itemTotal)


# Route to display item description
@app.route('/catalog/<string:category_name>/<string:item_name>')
def showItemDescription(category_name, item_name):
    """ Dislays the description for a selected item """
    category = session.query(Category).filter_by(name=category_name).one()
    creator = getUserInfo(category.user_id)
    item = session.query(CategoryItem).filter_by(name=item_name).one()
    if 'username' not in login_session:
        return render_template('publicitemdescription.html', item=item)
    else:
        return render_template('itemdescription.html', item=item)


# Route to add a new item
@app.route('/catalog/add/', methods=['GET', 'POST'])
def addItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form.get('item_category') == "other":
            category = Category(
                name=request.form['other_item_category'],
                user_id=login_session['user_id'])
            session.add(category)
            session.commit()

            newItem = CategoryItem(
                name=request.form['item_name'],
                description=request.form['item_description'],
                category=category,
                user_id=category.user_id)
            session.add(newItem)
            session.commit()
        else:
            category = session.query(Category).
            filter_by(name=request.form.get('item_category')).one()
            newItem = CategoryItem(
                name=request.form['item_name'],
                description=request.form['item_description'],
                category=category,
                user_id=category.user_id)
            session.add(newItem)
            session.commit()
        flash(newItem.name + " has been added successfully to the database!")
        return redirect(url_for('showCatalog'))
    else:
        categories = session.query(Category).all()
        return render_template('additem.html', categories=categories)

# Route to edit an item


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(CategoryItem).filter_by(name=item_name).one()
    if item.user_id != login_session['user_id']:
        return "<script>\
        function myFunction(){\
        alert('You are not authorized to edit this restaurant.\
        Please create your own item to edit it.')\
        }</script>\
        <body onload='myFunction()'></body>"
    if request.method == 'POST':
        # item = session.query(CategoryItem).filter_by(name = item_name).one()
        category = session.query(Category).filter_by(name=request.form.get('item_category')).one()
        if request.form['item_name']:
            item.name = request.form['item_name']
        if request.form['item_description']:
            item.description = request.form['item_description']
        if request.form['item_category']:
            item.category_id = category.id
        session.add(item)
        session.commit()
        flash(item_name + " has been edited successfully!")
        return redirect(url_for('showCatalog'))
    else:
        categories = session.query(Category).all()
        item = session.query(CategoryItem).filter_by(name=item_name).one()
        return render_template(
            'edititem.html',
            categories=categories,
            item=item)

# Route to delete an item


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(CategoryItem).filter_by(name=item_name).one()
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction(){\
        alert('You are not authorized to delete this restaurant. Please create\
        your own item to delete it.')}</script>\
        <body onload='myFunction()'></body>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash(item_name + " has been deleted successfully from the database!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteitem.html', item=itemToDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8075)
