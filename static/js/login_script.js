$(document).ready(function() { 
	console.log("Ready");
	//attach function to login submit button
	$('#loginForm').submit(function(e){
		//check to make sure that the form fields are filled out
		e.preventDefault();
		//obtain the form text values
		var username = $("#userName").val();
		var password = $("#password").val();
		if (username === "" | password === ""){//if the username and password aren't both filled in, display an error message
			$('.errorMessage').text("You must fill in your username and password")
			$('.errorMessage').show();
			return;
		}	
		else{//send post request to server to log the user in
			$.ajax({
				url: '../server/loginConfirm',
				type: 'POST',
				dataType: 'json',
				data: {user_name: username, password: password},
				success: function(data,textStatus, jqXHR){
					console.log(data);
					if (data.answer === "It matches"){//if the login was successful, load the user's home page
						url = formURL("home");
						console.log(url);
						location.href = url;
					}
					else if (data.answer === "It does not match"){//else if the password doesn't match the username, display error message
						$('.errorMessage').text("That password you entered does not match with your username. Please try again.");
						$('.errorMessage').show();
						return;
					}
					else if (data.answer == "User doesn't exist"){//else if the username does not exist, display error message
						$('.errorMessage').text("That username does not exist in our database. Please try again.");
						$('.errorMessage').show();
						return;
					}
					else {//else- other error conditions
						$('.errorMessage').text("Sorry, we are unable to log you in at this time.");
						$('.errorMessage').show();
						return;
					}
				},
				error: function(jqXHR, textStatus, errorThrown){//display error message with server error
					$('.errorMessage').text("Sorry, we are unable to log you in at this time.");
					$('.errorMessage').show();
					console.log(textStatus);
					console.log(errorThrown);
				}
			});
		}
	});
}); 

/**
    Function to creates an absolute link provided a string input relative to server/
**/

function formURL(redirect){
	var url =  document.URL;
	var last_char = url.indexOf('server') + 7;
	var sub_string = url.substr(0,last_char);
	//console.log(">>>>>>", url.indexOf('server'));
	console.log(">>>>>>", sub_string);
	return sub_string + redirect
	return url;
}