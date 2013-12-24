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

app = flask.Flask(__name__)

# Server reloads itself on code changes and gives you errors
app.debug = True

db = shelve.open("shorten_test.db")

# Project 1 Functions

###
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
@app.route('/home', methods=['GET'])
def getHome():
    """Returns homepage resource"""
    return flask.render_template(
            'home.html',
            username = session['username'])
###
# urlShorty:
# GET method returns html template for urlShorty
@app.route('/create', methods=['GET'])
def urlShorty():
    """Returns homepage resource"""
    return flask.render_template(
            'urlShortyForm.html')
###


@app.route('/register', methods=['GET'])
def getRegister():
    """Returns homepage resource"""
    return flask.render_template(
            'register.html')

# login:
# GET returns the login.html page
@app.route('/login', methods=['GET'])
def getLogin():
    """Returns homepage resource"""
    return flask.render_template(
            'login.html')

# GET returns the login.html page
@app.route('/twitter', methods=['GET'])
def getLogin():
    """Returns homepage resource"""
    return flask.render_template(
            'twittertutorial.html')
			
			

@app.route('/loginConfirm', methods=['POST'])
def loginConfirm():
    """Checks to make sure the user name and password are valid"""
    userName = str(request.form.get('user_name'))
    password = str(request.form.get('password'))
    session['username'] = userName
    return "true" 

app.secret_key = 'TESTING123TESTING456'


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

@app.route('/getAll', methods=['GET'])
def getAll():	
	return jsonify(answer = getAllQuery(request.args.get('userName')))

# lookupShortURL:
@app.route("/lookupShortURL", methods=['GET'])	
def lookupShortURL():
	return jsonify(answer =lookupShortURLQuery(request.args.get('shortURL')))

# addUser:
# return the user_name cookie to the nav
# TODO: return the user name to the top nav 
#REGISTER / CREATE ACCOUNT PAGE
@app.route("/addUser", methods=['POST'])
def addUser():
    userName = str(request.form.get('userName'))
    longURL = str(request.form.get('password'))
    response = addUser(user_name, password)
    return jsonify(answer =response)


# addURLQuery:
@app.route("/addShort", methods=['POST'])
def addShort():
	userName = str(request.form.get('userName'))
	longURL = str(request.form.get('longURL'))
	shortURL = str(request.form.get('shortURL'))
	response = addShortURLQuery(shortURL_input, longURL_input, session)
	return jsonify(answer =response)


	
	# Short:
# POST method associates long url with short url in dictionary
# GET method redirects to long url
###
@app.route("/short", methods=['POST'])

@app.route("/edit", methods=['POST'])
def editShort():
    shortURL = str(request.form.get('shortURL'))
    longURL = str(request.form.get('longURL'))
    deleteURLQuery(shortURL_input)
    shortURL = str(request.form.get('shortURL'))
    addShortURLQuery(shortURL_input, longURL_input, session)
    return ""


@app.route("/deleteShort", methods=['POST'])
def deleteShort():
    shortURL = str(request.form.get('shortURL'))
    return jsonify(answer = deleteURLQuery(shortURL_input))

# Short:
# POST method associates long url with short url in dictionary
# GET method redirects to long url
# ###
# @app.route("/short", methods=['POST'])
# def short_post():
#     """Creates a new association between the short name and the URL"""
#     longURL = str(request.form.get('longURL'))
#     shortURL = str(request.form.get('shortURL'))
#     db[shortURL] = longURL

#     ourResponse = '<p>Success! The original url: &#60' + longURL + '&#62 has been shortened to:</p>'
#     new_link = ' <a href="http://people.ischool.berkeley.edu/~chrisfan/server/short/'+shortURL+'"> Here is your new link </a>'
#     return jsonify(text = ourResponse, link=new_link, url = shortURL)

########
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

	


