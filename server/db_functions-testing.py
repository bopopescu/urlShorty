import json 
import random
import MySQLdb, _mysql
from passlib.hash import bcrypt


"""Connects to the specific database."""
def connect_db():   
	conn = MySQLdb.connect(host="localhost", user="urlShortyDb", passwd="metacrap",db="urlShortyDb")
    #conn.row_factory = dict_factory
	return conn


#REGISTER / CREATE ACCOUNT PAGE
def addUser(user_name_input, password_input):
	db = connect_db()
	cur = db.cursor()
	hashed = bcrypt.encrypt(password_input, bcrypt.gensalt())
	username_password = (user_name_input, hashed)
	query_text = "insert into testing_login (user_name, password) values ('%s','%s')" % username_password
	try:
		cur.execute(query_text)	
		db.commit()
		db.close()
		return "Add User success"
	except:
		db.rollback()
		return "There was a problem adding the record"


#LOGIN PAGE
def userValidate(user_name_input):
	db = connect_db()
	cur = db.cursor()
	user_name_query_text = "select user_name from testing_login where user_name ='%s'" % user_name_input
	cur.execute(user_name_query_text)
	result = cur.fetchone()[0]
	print result
	if result == None:
		return False
	elif user_name_input == result:
		return True
	db.close()

def loginConfirm(user_name_input, password_input):
	#check to see if the user exists
	check_user = userValidate(user_name_input)
	if check_user == False:
		return "User doesn't exist"	
	else:
		password_query_text = "select password from testing_login where user_name ='%s'" % user_name_input
		cur.execute(password_query_text)
		hashed = cur.fetchone()[0]
		print hashed
		print str(bcrypt.verify(password_input, hashed))
		if bcrypt.verify(password_input, hashed) == True:
			return "It matches"
		else:
			return "It does not match"
	db.close()

def returnJSON(result):
	json_list = []
	for items in result:
		json_element = {}
		json_element['shortURL'] = items[0]
		json_element['longURL'] = items[1]
		json_element['userID'] = items[2]
		json_list.append(json_element)
	return json_list	

def showAll():
	db = connect_db()
	cur = db.cursor()	
	query_text = "select * from links"
	cur.execute(query_text)
	result = cur.fetchall()
	db.close()
	return returnJSON(result)
	
def getAllQuery(username):
	db = connect_db()
	cur = db.cursor()	
	query_text = "select * from links where userID= '%s'" % username
	#print (sql_text)
	cur.execute(query_text)
	result = cur.fetchall()
	db.close()
	return returnJSON(result)

def lookupShortURLQuery(shortURL):
	db = connect_db()
	cur = db.cursor()	
	query_text = "select * from links where shortURL= '%s'" % shortURL
	#print (sql_text)
	cur.execute(query_text)
	result = cur.fetchall()
	db.close()
	return returnJSON(result)
	
# def editURLQuery(shortURL):
# 	db = connect_db()
# 	cur = db.cursor()		
# 	query_text = "delete from links where shortURL='%s'"%shortURL		
# 	print(query_text)	
# 	try:
# 		cur.execute(query_text)	
# 		db.commit()
# 		return "Delete URL Success"
# 	except:
# 		db.rollback()
# 		return "There was a problem in deleting the record."
# 	db.close()
# 	return 

	
def deleteURLQuery(shortURL):
	db = connect_db()
	cur = db.cursor()		
	query_text = "delete from links where shortURL='%s'"%shortURL		
	print(query_text)	
	try:
		cur.execute(query_text)	
		db.commit()
		return "Delete URL Success"
	except:
		db.rollback()
		return "There was a problem deleting the record."
	db.close()
	return 
	

def main():
	#addShortURLQuery1('user_name5', 'short_url5w', 'long_url5')
	#print showAll()
	#print getAllQuery("user_name5")
	#print(lookupShortURLQuery('link1333'))
	#print addUser('USER001', 'carraramarble')

	#print loginConfirm('USER001', 'kitchens')
	#print loginConfirm('USER002', 'kitchens')
	print userValidate('USER001')
	print userValidate('USER002')

	#deleteURLQuery('short_url5w')
	return
	
if __name__ == "__main__":
    #getAllQuery('user_name1')
	#lookupShortURL()
	main()