$(document).ready(function() { 
	console.log("Ready");
	$('#userLinks').hide();
	$('#tableHeaders').hide();
	//get user's URLs to display in a table
	$.ajax({
		url: '../getAll',
		type: 'get',
		//this needs to be taken out after testing
		dataType: 'json',
		success: showUserResults,
	});
/**
    Attaches click event to editLink that takes user to edit page for their URL
**/
	$("tbody").on('click', '.editLink', function(e){
		e.preventDefault;
		//traverse the DOM to obtain the short and long URLs
		var short_url = $(this).parent().next().next().text();
		var long_url = $(this).parent().next().text();
		//create the GET requst link to the edit page for the URL pair
		editPage = "edit?shortURL=" + short_url + "&longURL=" + long_url
		url = formURL(editPage)
		//open the edit page
		location.href = url;
	})

/**
    Attaches click event to deleteLink that lets user delete their URL pair
**/

	$("tbody").on('click', '.deleteLink', function(e){
		//alert('you are deleting');
		e.preventDefault();
		var short_url = $(this).parent().next().next().text();
		//post request to URL to delete the short url from the database
		$.ajax({
			url: '../deleteShort',
			type: 'post',
			data: {shortURL: short_url},
			dataType: 'json',
			success: confirmDelete,
			error: errorDelete
		});

	});
});

/**
    Function to display user's URL pairs in a table
**/

function showUserResults(data, textStatus, jqXHR){
	var url_response = data
	console.log(url_response.answer.length)
	//if the user doesn't have any URLs, hide the table
	if (url_response.answer.length === 0){
		$('#userLinks').hide();
		$('#tableHeaders').hide();
	}
	else {//else add the short and long links into the table
		$('#userLinks').show();
		$('#tableHeaders').show();
		$.each(data.answer, function(i,value){
			var short_url = value.shortURL;
			var long_url = value.longURL;
			var absolute_short = formURLNew(short_url);
			$('#userLinks').append("<tr class=userLink><td class='iconButtons'><a class='editLink' href='#''></a><a class='deleteLink' href='#''></a></td><td class='longLink'><a href='" + long_url + "'>" + long_url + "</a></td><td class='shortLink'><a href='" + absolute_short + "'>" + short_url + "</a></td></tr>");
			//$('#userLinks').append("<td class='iconButtons'><a class='editLink' href='#''></a><a class='deleteLink' href='#''></a></td>");
			//$('#userLinks').append("<td class='longLink'><a href='" + long_url + "'>" + long_url + "</a></td>");
			//$('#userLinks').append("<td class='shortLink'>" + short_url + "</td></tr>");
			//$('#userLinks').append("</tr>");
		});
	}
}

/**
    Function to check whether the server successfully deleted the URL pair
**/

function confirmDelete(data, textStatus, jqXHR){
	console.log(data);
	if (data.answer === "Success"){//if delete was successful, reload page from server to get refreshed results
		//reloads page from server
		//do we also want to display a message?
		location.reload(true);
	}
	else {//else show error message
		$(".errorMessage").text("Sorry! We are unable to delete your URL at this time.");
	}
}

/**
    Function to deal with errors for server delete
**/

function errorDelete(jqXHR, textStatus, errorThrown){
	console.log(errorThrown);
	$(".errorMessage").text("Sorry! We are unable to delete your URL at this time.");
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
	return sub_string + redirect;
	return url;
}

function formURLNew(redirect) {
    var url = document.URL;
    var last_char = url.indexOf('server') + 7;
    var sub_string = url.substr(0, last_char);
    //console.log(">>>>>>", url.indexOf('server'));
    console.log(">>>>>>", sub_string);
    return sub_string +'short/'+ redirect;
    return url;
}