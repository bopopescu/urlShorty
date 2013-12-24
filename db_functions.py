import json 
import random
import MySQLdb, _mysql
import bcrypt



## Ideally the access rights to the files will be controlled by the webserver prevening outside intrusion 
"""Connects to the specific database."""
def connect_db():   
	conn = MySQLdb.connect(host="localhost", user="urlShortyDb", passwd="metacrap",db="urlShortyDb")
    #conn.row_factory = dict_factory
	return conn

# Makes sure the user is actually in the 'testing_login' table
def userValidate(user_name_input):
	db = connect_db()
	cur = db.cursor()
	# user_name_query_text = "select user_name from testing_login where user_name ='%s'" % user_name_input
	user_name_query_text = "select user_name from testing_login where user_name =%s" 
	cur.execute(user_name_query_text, (user_name_input,))
	result = cur.fetchone()
	db.close()

	if result != None: 
		if user_name_input == result[0]:
			return True
		else:
			return False
	else: 
		return False

# Adds a new user to the 'testing_login' table 
def addUser(user_name_input, password_input):
	check_user = userValidate(user_name_input)
	db = connect_db()
	cur = db.cursor()
	result = ""

	if check_user == True:
		db.rollback()
		result = "User already exist"	
	else:
		hashed = bcrypt.hashpw(password_input, bcrypt.gensalt())
		username_password = (user_name_input, hashed)
		# query_text = "insert into testing_login (user_name, password) values ('%s','%s')" % username_password
		query_text = "insert into testing_login (user_name, password) values (%s,%s)" 
		try:
			cur.execute(query_text, username_password)	
			db.commit()
			db.close()
			result = "Add User success"
		except:
			db.rollback()
			result = "There was a problem adding the record"
	return result

# Checks if user exists and if password is valid run in __loginConfirm()__  in app.py 
def passwordValidate(user_name_input, password_input):
	#check to see if the user exists
	check_user = userValidate(user_name_input)
	result = ''
	if check_user == False:
		result = "User doesn't exist"	
	elif check_user == True:
		db = connect_db()
		cur = db.cursor()
		# password_query_text = "select password from testing_login where user_name ='%s'" % user_name_input
		password_query_text = "select password from testing_login where user_name =%s" 
		cur.execute(password_query_text, (user_name_input,))
		db.commit()
		#passwordDb = cur.fetchone()[0]
		#print passwordDb
		hashed = cur.fetchone()[0]
		if bcrypt.hashpw(password_input, hashed) == hashed:
			result = "It matches"
		else:
			result = "It does not match"
		db.close()
	else:
		result = "Error"
	return result

# Transforms 'links' table data into JSON
def returnJSON(result):
	json_list = []
	for items in result:
		json_element = {}
		json_element['shortURL'] = items[0]
		json_element['longURL'] = items[1]
		json_element['userID'] = items[2]
		json_list.append(json_element)
	return json_list	

# Add short URL if it doesn't already exist in the 'links' table
def addShortURLQuery(shortURL_input, longURL_input, userID):
	shortURLQuery = lookupShortURLQuery(shortURL_input)
	print shortURLQuery
	db = connect_db()
	cur = db.cursor()
	links_input = (shortURL_input, longURL_input, userID)
	# query_text = "insert into links (shortURL, longURL, userID) values ('%s','%s', '%s')" % links_input
	query_text = "insert into links (shortURL, longURL, userID) values (%s,%s, %s)" 
	result = ''

	if len(shortURLQuery) == 0:
		cur.execute(query_text, links_input)
		db.commit()
		db.close()
		result = "Success"
	elif len(shortURLQuery) >= 1:
		result = "Not available"
	else:
		result = "Error"
	return result

# Show everything in links
def showAll():
	db = connect_db()
	cur = db.cursor()	
	query_text = "select * from links"
	cur.execute(query_text)
	result = cur.fetchall()
	db.close()
	return returnJSON(result)

# Get all info from 'links' for a given 'username' 	
def getAllQuery(username):
	db = connect_db()
	cur = db.cursor()	
	# query_text = "select * from links where userID= '%s'" % username
	query_text = "select * from links where userID= %s" 
	#print (sql_text)
	cur.execute(query_text, (username,))
	result = cur.fetchall()
	db.close()
	return returnJSON(result)

# Lookup short URL
def lookupShortURLQuery(shortURL_input):
	db = connect_db()
	cur = db.cursor()	
	# query_text = "select * from links where shortURL= '%s'" % shortURL_input
	query_text = "select * from links where BINARY shortURL= %s" 
	#print (sql_text)
	cur.execute(query_text, (shortURL_input,))
	result = cur.fetchall()
	db.close()
	return returnJSON(result)

## Makes requests to the database to edit existing short URLs or create a new short url association with a long url
def editURLQuery(oldshortURL, newshortURL, newLong, userID):
	db = connect_db()
	cur = db.cursor()		
	
	if oldshortURL == newshortURL:
		return updateURL(oldshortURL, newLong)
	elif len(lookupShortURLQuery(newshortURL)) == 0:
			# print "adding new url"
			try:
				addShortURLQuery(newshortURL, newLong, userID)
				deleteURLQuery(oldshortURL)				
				return "Success"
			except:
				return "Oops! Something went wrong!"
	else:
		return "Not available"
	return 

## Update an existing short URL with a new long url
def updateURL(	shortURL, newLongURL):
	db = connect_db()
	cur = db.cursor()			
	new_links = (newLongURL, shortURL)
	# query_text = 'update links set links.longURL="%s" where links.shortURL="%s"' % new_links
	query_text = 'update links set links.longURL=%s where links.shortURL=%s' 
	try:
		cur.execute(query_text,  new_links)
		db.commit()
		db.close()
		return "Success"
	except:
		db.rollback()
		db.close()
		return "Error"
	return
	
# Delete 'shortURL_input' 	
def deleteURLQuery(shortURL_input):
	db = connect_db()
	cur = db.cursor()		
	# query_text = "delete from links where shortURL='%s'"%shortURL_input		
	query_text = "delete from links where shortURL=%s"	
	# print query_text
	try:
		cur.execute(query_text, (shortURL_input,)	)	
		db.commit()
		return "Success"
	except:
		db.rollback()
		return "Error"
	db.close()
	return 
	

def main():
	#addShortURLQuery1('user_name5', 'short_url5w', 'long_url5')
	#print showAll()
	# print getAllQuery("christest")
	
	#print addUser('USER004', 'gobears')
	# print addUser('USER007', 'zebracake')
	# print passwordValidate('USER007', 'zebracake')
	# print passwordValidate('USER008', 'zebracake')
	
	
	# print editURLQuery('shorturltestA', 'shorturltestA', 'thisshouldchange', 'christest2')
	
	#### Checking SQL escaping	
	# print userValidate('USER00w7')
	# print addShortURLQuery('food', 'http://food.com', 'fanman')
	# print deleteURLQuery('christest')
	print lookupShortURLQuery('news')
	# print passwordValidate('christest2', 'metacrap1234adsf')
	# print addUser('USER004', 'gobears')
	
	
	# print updateURL('zotwhm', 'thisisatest')
	#print passwordConfirm('USER004', 'gobears')
	#print passwordConfirm('USER002', 'kitchens')
	# print userValidate('USER004')
	
	
	#deleteURLQuery('short_url5w')
	return
	
if __name__ == "__main__":
    #getAllQuery('user_name1')
	#lookupShortURL()
	main()