$(document).ready(function() { 
	console.log("Ready");
	//attach function to login submit button
	$('#loginForm').submit(function(e){
		e.preventDefault();
		$(".errorMessage").hide();
		//get the form text values
		var username = $("#userName").val();
		var password = $("#password").val();
		var password_confirm = $("#passwordConfirm").val();
		//if any of the form fields are blank, show an error message
		if (username === "" | password === "" | password_confirm === ""){
			$('.errorMessage').text("Please fill in all of the fields.")
			$('.errorMessage').show();
			return false;
		}	
		if (!validateName(username)){//if the username does not meet the requirements, display an error message
			$('.errorMessage').text("Your username must be between 6 and 12 characters long (letters and numbers only)")
			$('.errorMessage').show();
			return false;
		}
		if (!validatePassword(password)){//if the password does not meet the requirements, display an error message
			$('.errorMessage').text("Your password must be between 8 and 16 characters long (letters and numbers only)")
			$('.errorMessage').show();
			return false;
		}
		if (password != password_confirm){//if the two passwords don't match, display an error message
			$('.errorMessage').text("Your passwords do not match. Please re-enter")
			$('.errorMessage').show();
			return false;
		}
		else{//if everything is valid, send post request to server to register the user and log them in
			$.ajax({
				url: '../server/registerConfirm',
				type: 'POST',
				dataType: 'json',
				data: {user_name: username, password: password},
				success: function(data,textStatus, jqXHR){
					console.log(data);
					if (data.answer === "Add User success"){//if the registration was succesful, open the user's home page
						url = formURL("home");
						console.log(url);
						location.href = url;
					}
					else if (data.answer === "User already exist") {//if the username was already taken, display an error
						$(".errorMessage").text("That username has already been taken. Please choose another.");
						$(".errorMessage").show();
					}
					else {//else (other errors), display an error message
						$(".errorMessage").text("Sorry, we are unable to register you at this time.")
						$(".errorMessage").show();
					}
				},
				error: function(jqXHR, textStatus, errorThrown){//function to display error given server error
					$(".errorMessage").text("Sorry, we are unable to register you at this time.") 
					$(".errorMessage").show();
					console.log(textStatus);
					console.log(errorThrown);
					return false;
				}
			});
		}
	});
}); 

/**
    Function to validate username 
**/

function validateName(username){
	//username must be between 6 and 16 characters (letters and numbers only)
	var validChars = /^[A-Za-z0-9]{6,12}$/;
	if (!validChars.test(username))
		return false;
	else
		return true;
}

/**
    Function to validate password
**/

function validatePassword(password) {
	//password must be between 8 and 16 characters (letters and numbers)
	var validChars = /^[A-Za-z0-9]{8,16}$/;
	if (!validChars.test(password))
		return false;
	else
		return true;
}

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