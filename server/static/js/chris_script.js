$(document).ready(function() { 
	console.log("Ready does this change");


/**
	Tiffany: The return value from 'getAllfromFlask' is something called a "Deferred Object". 
	I am doing to show how to separate out the code that actually calls the AJAX function.
	
	To work with Deferred Objects you can use the (DeferredObject).done() method. Basically the data returned from the AJAX call is "data" fed into the done method
	
	All values returned from the AJAX calls need to be called data.answer. I am basically returning a simple JSON object of type {answer: SQLanswer}
**/		
	$("#show_all").click( function(){
		getAllfromFlask($("#user_id").val()).done(function(data){
			console.log(data);
			$("#showAll").empty();
			$("#showAll").append("<p> AJAX getAllfromFlask Completed </p>");
			$.each(data.answer, function(index, value){			
				console.log(value);
				html_string = "<p>";
				html_string = html_string + JSON.stringify(value) + "</p>"
				$("#showAll").append(html_string);
			});
		});			
	return false;
	});

/**
	lookupShortURL
**/	
	$("#check_shortURL").click (function(){
		//console.log("checkShortURL>>>>>>.");
		 lookupShortURL($("#shortURL").val()).done(function(data){			
			$("#showShortURL").empty();	
			
			if(data.answer.length >0){ //if the array is empy there are no corresponding URLs
				result = data.answer[0]; // the SQL row is in the first element of array
				$("#showShortURL").append("<p> AJAX from lookupShortURL </p>");
				html_string = "<p> shortURL Answer: "+ result.shortURL + " is [" + result.longURL +"] </p>";						
				$("#showShortURL").append(html_string);
			}else{
				html_string = "<p> There are no links associated</p>";	
				$("#showShortURL").append(html_string);				
			}
		});
		return false;
	});
	
	$("#add_shortURL").click(function(){
		userName = $("#user_id").val();
		shortURL = $("#shortURL").val();
		longURL =$("#longURL").val();
		//console.log(userName, shortURL, longURL);
		addShortURL(userName, shortURL, longURL).done(function(data){
			console.log("Success addShortURL");
			console.log(data);
		});
	});
	
	$("#delete_shortURL").click(function(){		
		shortURL = $("#shortURL").val();		
		//console.log(userName, shortURL, longURL);
		deleteShortURL(shortURL).done(function(data){
			//console.log("Success deleteShortURL");
			console.log(data);
		});
	});
	
});

/**
	getAllfromFlask is an AJAX call that returns and JSON object corresponding to the short/long urls associated with a username
	The HTTP [get] requires a parameter "user_name" that specifies the string for the user name
	Return value to AJAX call to FLASK is a deferred object.
	The data returned from the AJAX function will be an array of JSON Objects of type {'shortURL': value, 'longURL': value, 'userID': value}
**/
function getAllfromFlask(userName){
	return $.ajax({
		url: '../getAll',
		type: 'get',
		data: {user_name: userName}, 
		dataType: 'json',
		success: function(data,textStatus, jqXHR){				
			//console.log("getAllfromFlask AJAX Call Success");
		}							
	});
}
/**
	The data returned from the AJAX function will be an array of JSON Objects of type {'shortURL': value, 'longURL': value, 'userID': value}
**/
function lookupShortURL(shortURLInput){
	//console.log(">>>>>>>>>>>>>",shortURLInput);
	return $.ajax({
		url: '../server/lookupShortURL',
		type: 'get',
		data: {shortURL: shortURLInput}, 
		dataType: 'json',
		success: function(data,textStatus, jqXHR){		
			console.log("lookupShortURL AJAX Call Success");
			console.log(data)			
		}
	});
}

function addShortURL(usernameinput, shortURLinput, longURLinput){
		return $.ajax({
		url: 'static/js/Twitter/addShort',
		type: 'POST',
		data: {userName: usernameinput,shortURL: shortURLinput, longURL:longURLinput}, 
		dataType: 'json',
		success: function(data,textStatus, jqXHR){		
			console.log("lookupShortURL AJAX Call Success");
			console.log(data)
		}
	});
}

function deleteShortURL(shortURLinput){
		return $.ajax({
		url: '../server/deleteShort',
		type: 'POST',
		data: {shortURL: shortURLinput}, 
		dataType: 'json',
		success: function(data,textStatus, jqXHR){		
			//console.log("lookupShortURL AJAX Call Success");
			//console.log(data)
		}
	});
}