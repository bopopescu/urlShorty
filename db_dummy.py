import json 
import random


def getAllQuery(username):
	json_file = open ('dummy_data1.json', 'r')
	json_data = json.load(json_file)
	answer = {}
	for key,value in json_data.items():
		print(value)
		if value[u'userID'] == username.encode('utf8'):
			answer[key]=value
	#print(answer)
	json_file.close()
	return answer

def lookupShortURLQuery(shortURL):
	answer = {}
	answer["result"] = "false"
	answer["longURL"] =""
	json_file = open ('dummy_data1.json', 'r')
	json_data = json.load(json_file)
	
	for key,value in json_data.items():				
		if value[u'shortURL'] == shortURL.encode('utf8'):
			answer['longURL']=value[u'longURL']
			answer['result']="true"	
	json_file.close()
	return  answer
	
def addShortURLQuery(userID_input, shortURL_input, longURL_input):
	json_file = open ('dummy_data1.json', 'r')	
	json_data = json.load(json_file)	
	json_file.close()
	number = str(random.randrange(1000))
	key_string = 'key' + number
	value_json = {}
	value_json['userID']= userID_input
	value_json['shortURL']=shortURL_input
	value_json['longURL']=longURL_input
	print("Key:" + key_string + " Value: " + json.dumps(value_json))
	json_data[key_string]=value_json	
	json_write = open('dummy_data1.json','w')
	json_write.write(json.dumps(json_data))
	json_write.close()
	
	return value_json

	
if __name__ == "__main__":
    #getAllQuery('user_name1')
	#lookupShortURL()
	addShortURLQuery('user_name5', 'short_url5', 'long_url5')