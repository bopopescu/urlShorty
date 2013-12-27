#!/usr/bin/env python

import shelve
import json
from db_functions import *
from pprint import pprint 
from subprocess import check_output
import flask
from flask import request, abort, jsonify, session
from os import environ
from sqlite3 import dbapi2 as sqlite3
from functools import wraps

app = flask.Flask(__name__)

# Server reloads itself on code changes and gives you errors
app.debug = True

db = shelve.open("shorten_test.db")

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return test(*args, **kwargs)
        else:
            return getLogin()
    return wrap

### FLASK routers
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
@app.route('/home', methods=['GET'])
@login_required
def getHome():
    """Returns homepage resource"""
    return flask.render_template(
            'home.html',
            username = session['username'])

## Route to Login Page
@app.route('/login', methods=['GET'])
def getLogin():
    """Returns homepage resource"""
    return flask.render_template(
            'login.html')

## Route to sets user session if username and password match
@app.route('/loginConfirm', methods=['POST'])
def loginConfirm():
    """Checks to make sure the user name and password are valid"""
    userName = str(request.form.get('user_name'))
    password = str(request.form.get('password'))
    #check to make sure they are valid. For testing cookies, I've skipped this
    response = passwordValidate(userName, password)
    if response == "It matches":
        session['username'] = userName
    return jsonify(answer = response)

## Route to registration page	
@app.route('/register', methods=['GET'])
def getRegister():
    """Returns homepage resource"""
    return flask.render_template(
            'register.html')

## Route to sets user session if username and password match
@app.route('/registerConfirm', methods=['POST'])
def registerConfirm():
    """Checks to make sure the user name and password are valid"""
    userName = str(request.form.get('user_name'))
    password = str(request.form.get('password'))
    #check to make sure they are valid. For testing cookies, I've skipped this
    response = addUser(userName, password)
    if response == "Add User success":
        session['username'] = userName
    return jsonify(answer = response)

##  Logout
@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    session.pop('username', None)
    #flash('You were logged out')
    return getLogin()

## Route to the edit.html template	
@app.route('/edit', methods = ['GET'])
@login_required
def edit():
    shortURL = str(request.args.get('shortURL'))
    longURL = str(request.args.get('longURL'))
    return flask.render_template(
        'edit.html',
        username = session['username'],
        shortURL = shortURL,
        longURL = longURL)

## Twitter tester
@app.route('/twitter', methods = ['GET'])
def twitter():
    return flask.render_template(
        'twittertutorial.html')		
##Route to the template to generate new short URLS		
@app.route('/urlShortyForm', methods = ['GET'])
@login_required
def urlShortyForm():
    return flask.render_template(
        'urlShortyForm.html',
        username = session['username'],
        )
####################### HTTP Calls for Database Requests
		
## Gets all short URLs for a given user session
@app.route('/getAll', methods=['GET'])
def getAll():   
    #needs to take in session object eventually
    user_name = session['username']
    return jsonify(answer = getAllQuery(user_name))
	
# addURLQuery:
@app.route("/addShort", methods=['POST'])
def addShort():
    # userName = str(request.form.get('userName'))
    userName = session['username']
    longURL = str(request.form.get('longURL'))
    shortURL = str(request.form.get('shortURL'))
    #response = "Success"
    response = addShortURLQuery(shortURL, longURL, userName)
    return jsonify(answer =response)

#I got this from 
app.secret_key= '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


#########################################FLASK Code to handle calls to database##################################################

# chris
# demonstration code to show how to work with the various FLASK http requests for data from database
@app.route('/chris', methods=['GET'])
def testChris():    
    return flask.render_template(
            'chris_test.html')
###	

# getAll:
#GET returns JSON object corresponding to all database rows associated with a user
# Requires "user_name" parameter 


# lookupShortURL:
@app.route("/lookupShortURL", methods=['GET'])	
def lookupShortURL():
	return jsonify(answer =lookupShortURLQuery(request.args.get('shortURL')))

# addUser:
# 
@app.route("/addUser", methods=['POST'])
def addUser1():
    userName = str(request.form.get('user_name'))
    longURL = str(request.form.get('password'))
    response = addUser(user_name, password)
    return jsonify(answer =response)


# @app.route("/edit", methods=['POST'])
# def editShort():
    # oldShort = str(request.form.get('oldShort'))
    # newShort = str(request.form.get('newShort'))
    # newLong = str(request.form.get('newLong'))
    # if oldShort == newShort:
        # deleteURLQuery(shortURL)
    # shortURL = str(request.form.get('shortURL'))
    # addShortURLQuery(shortURL, longURL, session)
    # return ""

## Function makes a request for the database to delete a short URL	
@app.route("/deleteShort", methods=['POST'])
def deleteShort():
	shortURL = str(request.form.get('shortURL'))
	return jsonify(answer = deleteURLQuery(shortURL))

## Short:
# POST method associates long url with short url in dictionary
# GET method redirects to long url

@app.route("/short/<shortName>", methods=['GET'])
def short_get(shortName):
    """Redirects short name to URL or trigger 404 error if there is no association """
    shortName = str(shortName)
    answer = lookupShortURLQuery(shortName)
    
    if len(answer) ==0:
        abort(406)
    else:
        print "There is an existing url: ", answer
        destination = answer[0]['longURL']
        app.logger.debug("Redirecting to " + destination)
    return flask.redirect(destination)

## Processes requests to update an existing short URL	
@app.route("/updateShort", methods=['POST'])
def editURLRequest():
    oldShort = str(request.form.get('oldShort'))
    newShort = str(request.form.get('newShort'))
    newLong = str(request.form.get('newLong'))
    username = session['username']
    print ">>>>>>>>", "oldshort: ", oldShort, "newshort: ", newShort, "newlong:" , newLong
    return jsonify(answer = editURLQuery(oldShort,newShort,newLong, username))

## Generate errors for invalid page requests 
@app.errorhandler(404)
#Define function for rendering HTML template for a 404 error
def page_not_found(error):
    """Call custom 404 error page upon 404 error"""
    return flask.render_template(
        '404error.html'), 404

## Generate errors for invalid short url http requests
@app.errorhandler(406)
def page_not_found(error):
    """Call custom 404 error page upon 404 error"""
    return flask.render_template(
        'not_a_short.html'), 404		
		
if __name__ == "__main__":
    #runs on specified port
    app.run(port=int(environ['FLASK_PORT']))

######################################################################################3	

	


