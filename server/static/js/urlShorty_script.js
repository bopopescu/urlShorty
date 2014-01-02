$(document).ready(function() { 
	console.log("Ready");
	//hide divs to be populated later
	$('.suggestionBox').hide();
	$('#generated').hide();
	//disable the submit button
	$('#GO').attr('disabled', true);
 /**
    Do real-time validation of short URL
**/
	$('#NEW_URL').keyup( function (){
		var isValid = false;
		//hide the error message
		$(".errorMessage").hide();
		//get the value of the new URL as it is typed
		var new_url_text = $('#NEW_URL').val();	
		//disable the GO button if no shortURL text has been entered
		if (new_url_text.length === 0){
			$('#GO').attr('disabled', true);
		}
		else {
			//see if any of the characters in the new URL are not allowed
			for(var counter = 0; counter < new_url_text.length; counter ++){
				if (validate(new_url_text.charAt(counter))){
					isValid = true;
				}else{
					isValid = false;	
					break;
				}
			}				
			if(isValid){ // Show or Hide information for valid or invalid inputs
				//if valid, enable the submit button
				$('#GO').attr('disabled', false);
			}else{ //else show error message and disable submit button
				$(".errorMessage").text("Letters only, please!").show();
				$('#GO').attr('disabled', true);
			}	
		}
	});
/**
    Generate random URL on button click and make sure that it doesn't already exist in the database
**/
	$('#RANDOM').click(function(e){
		//prevent submit
		e.preventDefault();
		$(".suggestionBox").hide();
		$(".errorMessage").hide();
		$("#generated").hide();
		//generated random URL
		var new_string = generateRandomURL();
		//check with server to make sure this random URL hasn't already been taken. If it has been taken, generated a new one and repeat.
		while (true){
			invalid = checkURL(new_string);
			//if the shortURL is already taken, generate a new one
			if (invalid){
				new_string = generateRandomURL();
			}
			//once the URL has been validated, end loop and at short URL to form
			else {
				$('#NEW_URL').val(new_string);
				$('#GO').attr('disabled', false);
				break;
			}
		}
	});
/**
    Generate suggested URLs on button click using Twitter API and allow user to pick one as the short URL
**/
	$('#SUGGESTIONS').click(function(e) {
		e.preventDefault();
		$(".suggestionBox").hide();
		$(".suggestionBox").empty();
		$(".suggestionBox").append('<div>Twitter Suggestions:</div>')
		$(".errorMessage").hide();
		$("#generated").hide();
		//get the value of the original URL
		var text = $('#ORIGINAL_URL').val();
		if (text == ""){ //show error message if the user hasn't entered a long URL yet
			$(".errorMessage").text("Enter your original URL to get short URL suggestions.");
			return;
		}
		else { //else generate suggested short URLs from twitter based on the web page's title
			console.log("URLShorty suggestions for url:", text);        
        	getURLHeadInfo(text).done(function (data) {
        		// console.log(data);
				
				rankFunction(data.title).then(function (stuff){});
				
				if(data.keywords){//if keywords were returned, split them into an array and input them into giveSuggestions function to filter out URLS that have already been used
					var suggestions_all = data.keywords.split(",");
					// giveSuggestions(suggestions_all);
				}
				// else {//if no keywords were returned, inform user that recommendations are not possible at this time
				// 	$(".errorMessage").text("Sorry! We don't have any suggestions for that URL.");
				// 	$(".errorMessage").show();
				// }
			});
		}

	});
/**
    Attaches click event to suggestion boxes of short URLs. When user selects a suggested short URL, it gets populated in the form
**/
	$(".suggestionBox").on('click', '.suggestedShort', function(e){
		e.preventDefault;
		var choice = $(this).text();
		$('#NEW_URL').val(choice);
		$('#GO').attr('disabled', false);

	});

/**
    Attaches click event to GO button to submit short and long URLs to server
**/

	$('#GO').click(function(e) {  
		e.preventDefault();
		$(".suggestionBox").hide();
		$(".errorMessage").hide();
		$("#generated").hide();
		//set global variables for the original and new URLs submitted to server so they can be used later to send to the edit page
		window.oldUrlValue = $('#ORIGINAL_URL').val();
		window.newUrlVal = $('#NEW_URL').val();
		if (oldUrlValue === ""){//make sure the oldURL has been entered, otherwise show error message
			$(".errorMessage").text("Please enter a long URL");
			$(".errorMessage").show();
			return;
		}
		else {//if inputs are valid, send ajax call to server to add values to the database
			$.ajax({
				url: '../addShort',
				type: 'POST',
				dataType: 'json',
				data: {longURL: oldUrlValue, shortURL: newUrlVal},
				success: function(data,textStatus, jqXHR){	
					if (data.answer === "Success"){//if addition was successful, show the results on the page
						$('#generated').show();
						$('#NEW_URL_ENTRY').text(newUrlVal);
					}
					else if (data.answer === "Not available") {//if the short URL was taken, display error message
						$('.errorMessage').text("Oops! Somebody beat you to it. Please pick another short URL.");
						$(".errorMessage").show();
						return;
					}
					else {//else if something else went wrong
						$('.errorMessage').text("Oops! Something went wrong!");
						console.log(data);
						$(".errorMessage").show();
						return;
					}	
				},
				error: function(data, textStatus, jqXHR){
					$('.errorMessage').text("Oops! Something went wrong!");
					console.log(data);
					$(".errorMessage").show();
					return;
				} 	
			});						
		}
	});

/**
    Attaches click event to change URL button to allow user to edit the URL association they just made
**/
	$('#changeURL').click(function(e) {
		e.preventDefault();
		//generate relative link to edit URL page
		editPage = "edit?shortURL=" + window.newUrlVal + "&longURL=" + window.oldUrlValue;
		url = formURL(editPage)
		console.log(url);
		//open the edit URL page
		location.href = url;
	});
});

/**
    Function to take in keywords received from twitter program, find the ones that haven't been taken, and show them to user for selection
**/
function giveSuggestions(suggestions_all){
	var valid_suggestions = [];
	//loop through each keyword and, if it hasn't been used yet as a short URL add it to valid_suggestions
	for (var i=0; i<suggestions_all.length; i++){
		var suggestion_short = stripSpaces(suggestions_all[i]);
		//if the URL hasn't been taken, add it to valid_suggestions
		var something = checkURL(suggestion_short);
		//console.log(something);
		if (!checkURL(suggestion_short)){
			if (suggestion_short != ""){
				valid_suggestions.push(suggestion_short);
			}
		}
	}
	if (valid_suggestions.length === 0){//if there were no valid suggestions, show error message
		$(".errorMessage").text("Sorry! We don't have any suggestions for you right now.");
	}
	else {//else loop through each valid suggestion and display it on the page
		$.each(valid_suggestions, function(i,value){
			//console.log(value);
			$('.suggestionBox').show();
			$('.suggestionBox').append('<a href="#" class="suggestedShort">' + value + '</a>')
		});
	}
}

/**
    Function to display error if Twitter doesn't return any results
**/
function showTwitterError() {

    $(".errorMessage").text("Sorry! We don't have any suggestions for you right now.");
    $(".errorMessage").show();

}

/**
    Function to check with server to make sure the short URL hasn't been used yet
**/


function checkURL(short){
	$.ajax({
		url: '../lookupShortURL',
		type: 'GET',
		dataType: 'json',
		data: {shortURL: short},
		success: function(data, textStatus, jqXHR){
			//if the shortURL doesn't yet exist, return false
			//console.log(data);
			if (!data.answer){
				return false;
			}
			//else return true
			else {
				return true;
			}
		}
	});
}

/**
    Function to creates an absolute link provided a string input relative to server/
**/

function formURL(text){
	var url =  document.URL;
	var last_char = url.indexOf('server') + 7;
	var sub_string = url.substr(0,last_char);
	//console.log(">>>>>>", url.indexOf('server'));
	console.log(">>>>>>", sub_string);
	return sub_string + text;
}

/**
    Create a regular expression to validate whether each character in the short URL is a letter
    Note that we are not validating the whole string- we are checking to make sure each letter is valid
   **/

function validate(text){
	var validChars = /[A-Za-z]/;	
	if(!validChars.test(text))
		return false;
	else
		return true;
}

/**
    Genereate a random string comprized of six random alphabetical characters
**/

function generateRandomURL(){
	var randomString = '';	
	var getRandomChar = getRandomizer(97, 122);
	
	for( var counter = 0 ; counter < 6; counter ++){
		randomString +=  String.fromCharCode(getRandomChar());
	}
	return randomString;
}

/**
    Random Number Generator
**/

function getRandomizer(bottom, top) {
    return function() {
        return Math.floor( Math.random() * ( 1 + top - bottom ) ) + bottom;
    }
}

/**
    Function used by suggestion engine 
**/

function stripSpaces(phrase) {
	var noSpace = phrase.split(" ").join();
	var word = noSpace.replace(/[^A-Za-z]/g, '');
	return word
}

