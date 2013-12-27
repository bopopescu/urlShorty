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

###
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
@app.route('/home', methods=['GET'])
@login_required
def getHome():
    """Returns homepage resource"""
    return flask.render_template(
            'home.html',
            username = session['username'])

# login:
# GET returns the login.html page
@app.route('/login', methods=['GET'])
def getLogin():
    """Returns homepage resource"""
    return flask.render_template(
            'login.html')

@app.route('/loginConfirm', methods=['POST'])
def loginConfirm():
    """Checks to make sure the user name and password are valid"""
    userName = str(request.form.get('user_name'))
    password = str(request.form.get('password'))
    #check to make sure they are valid. For testing cookies, I've skipped this
    session['username'] = userName
    response = "It matches"
    #response = "It does not match"
    #response = "User doesn't exist"
    #response = ""
    return jsonify(answer = response)

@app.route('/register', methods=['GET'])
def getRegister():
    """Returns homepage resource"""
    return flask.render_template(
            'register.html')

@app.route('/registerConfirm', methods=['POST'])
def registerConfirm():
    """Checks to make sure the user name and password are valid"""
    userName = str(request.form.get('user_name'))
    password = str(request.form.get('password'))
    #check to make sure they are valid. For testing cookies, I've skipped this
    session['username'] = userName
    response = "Add User success"
    #response = "User taken"
    #response = ""
    #response = 
    return jsonify(answer = response)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    session.pop('username', None)
    #flash('You were logged out')
    return getLogin()

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

@app.route('/urlShortyForm', methods = ['GET'])
@login_required
def urlShortyForm():
    return flask.render_template(
        'urlShortyForm.html',
        username = session['username'],
        )

@app.route('/getAll', methods=['GET'])
def getAll():   
    #needs to take in session object eventually
    return jsonify(answer = getAllQuery(request.args.get('user_name')))

# addURLQuery:
@app.route("/addShort", methods=['POST'])
def addShort():
    userName = str(request.form.get('userName'))
    longURL = str(request.form.get('longURL'))
    shortURL = str(request.form.get('shortURL'))
    response = "Success"
    #response=addShortURLQuery(userName, shortURL, longURL)
    return jsonify(answer =response)

#I got this from a demo site, we need to replace it with our own random value
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
# FORM NAME????
@app.route("/addUser", methods=['POST'])
def addUser():
    userName = str(request.form.get('user_name'))
    longURL = str(request.form.get('password'))
    response = addUser(user_name, password)
    return jsonify(answer =response)



@app.route("/deleteShort", methods=['POST'])
def deleteShort():
	shortURL = str(request.form.get('shortURL'))
	return jsonify(answer = deleteURLQuery(shortURL))
# Short:
# POST method associates long url with short url in dictionary
# GET method redirects to long url
###
@app.route("/short", methods=['POST'])
def short_post():
    """Creates a new association between the short name and the URL"""
    longURL = str(request.form.get('longURL'))
    shortURL = str(request.form.get('shortURL'))
    db[shortURL] = longURL

    ourResponse = '<p>Success! The original url: &#60' + longURL + '&#62 has been shortened to:</p>'
    new_link = ' <a href="http://people.ischool.berkeley.edu/~chrisfan/server/short/'+shortURL+'"> Here is your new link </a>'
    return jsonify(text = ourResponse, link=new_link, url = shortURL)


@app.route("/short/<shortName>", methods=['GET'])
def short_get(shortName):
    """Redirects short name to URL or trigger 404 error if there is no association """
    shortName = str(shortName)
    if not shortName in db:
        abort(404)
    else:
        destination = db.get(shortName)
        app.logger.debug("Redirecting to " + destination)
    return flask.redirect(destination)



# Project 1 Functions

@app.errorhandler(404)
#Define function for rendering HTML template for a 404 error
def page_not_found(error):
    """Call custom 404 error page upon 404 error"""
    return flask.render_template(
        '404error.html')


if __name__ == "__main__":
    #runs on specified port
    app.run(port=int(environ['FLASK_PORT']))

######################################################################################3	

	


