$(document).ready(function() { 
	console.log("Ready");
	formURL('sample');
	$('#NEW_URL_ENTRY').hide();

    // Create a realtime validation of the new url string by validating the new url upon new character key press
	$('#NEW_URL').keyup( function (){
		//console.log($('#NEW_URL').val());
		var isValid = false;
		$(".error").hide();
		$("#NEW_URL").after('');
		
		var new_url_text = $('#NEW_URL').val();	
		for(var counter = 0; counter < new_url_text.length; counter ++){
			if (validate(new_url_text.charAt(counter))){
				isValid = true;
			}else{
				isValid = false;	
				break;
			}
		}				
		if(isValid){ // Show or Hide information for valid or invalid inputs
			$("#NEW_URL").after('<span class="error">Looking good!</span>');
		}else{
			$("#NEW_URL").after('<span class="error">Letters only, please!</span>');
		}				
	});
	
	$('#GO').click(function() {  
		$(".error").hide();
		var invalid = false;
		var validChars = /[A-Za-z]+$/;
 
		var newURLVal = $("#NEW_URL").val();
		if(newURLVal == '') {
			$("#NEW_URL").after('<span class="error">Enter desired text or click "RANDOM" below.</span>');
			invalid = true;			
		}
 
		else if(!validChars.test(newURLVal)) {
			$('#NEW_URL').after('<span class="error">Letters only, please!</span>');
			invalid = true;		  
			
		}
		if(invalid == false) { 
			var oldUrlValue = $('#ORIGINAL_URL').val();
			
			// Creat the AJAX Post call to the running instance of app.py 
			$("#NEW_URL").after('<span class="error"> Yay!</span>');	
			$.ajax({
				url: '../server/short',
				type: 'POST',
				dataType: 'json',
				data: {longURL: oldUrlValue, shortURL: newURLVal},
				success: function(data,textStatus, jqXHR){					
					//console.log(data);
					$('#NEW_URL_ENTRY').show();
					$('#NEW_URL_ENTRY').empty(); // Clear out response information 

					var new_url = formURL(data.url); // Generate the new absolute URL for the shorted URL
					var string = '<a href="' + new_url + '">' + new_url + '</a>';
                    //console.log(">>>>>>>>>", string)
                    $('#NEW_URL_ENTRY').append(data.text); // Append to the DOM
                    $('#NEW_URL_ENTRY').append(string);
				}							
			});

		}
		
		return false;
	});
    /**
    Generate a random string of alphabetical letters
    **/
	$('#RANDOM').click(function(){
		var new_string = generateRandomURL()
		console.log('String = ' , new_string);
		//$('#NEW_URL').val =  generateRandomURL();
		$('#NEW_URL').val(new_string);
		return false;
	});
	
});

/**
    Create an absolute link to the newly created shortenur. 
    forURL() assumes the patron is running the home.html from within a running app.py instance
    It grabs the local host information to append the newly create URL short string (/server/new_shortened_url)
**/

function formURL(text){
	var url =  document.URL;
	var last_char = url.indexOf('server') + 7;
	var sub_string = url.substr(0,last_char);
	//console.log(">>>>>>", url.indexOf('server'));
	console.log(">>>>>>", sub_string);
	return sub_string + 'short/'+ text;
}

/**
    Create a regular expression to validate whether the string is composed of entirely chracters
**/

function validate(text){
	var validChars = /[A-Za-z]+$/;	
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

