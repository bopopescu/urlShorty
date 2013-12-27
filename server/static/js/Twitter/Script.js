/**

**/
$(document).ready(function () {
    console.log("Ready");
    
    //getURLHeadInfo(temp);

    $("#tweet-tag-suggest").click(function () {
        var text = $("#tweet-text").val();
	
        console.log("Getting suggestions for url:", text);        
        getURLHeadInfo(text).done(function (data) {
			if(data.keywords){
				console.log("Keywords Retrieved", data.keywords);
			}
			rankFunction(data.title).resolve().then(function (stuff) {
			    console.log("does this work???????????????????????????????");
			});

            //rankFunction(data.title).done(function (data) {
			//    console.log("Resolve First Deferred Pipe()");
			//    console.log("This is data:")
			//    data.resolve();
			//    //console.log( data);
			//});
			
        });        
    });

});

function getURLHeadInfo(url_input) {
        
    return $.ajax({
        type: "post",        
        dataType: "json",
        url: "http://people.ischool.berkeley.edu/~chrisfan/twitter/_js/headerProxy.php",
        data: { 'urlname': url_input },
        error: function(jqXHR, testStatus, error){
            console.log("error");
            console.log(testStatus);            
        },
        success: function (data, status, xhr) {
            console.log("Call successful retreive HTTP header tags");
            console.log(data.title);
            //console.log(data.keywords);
            //console.log(data.description);
        }
    });
}

function test() {
    var request = new XMLHttpRequest();
    request.open('GET', 'http://xdr.example.net/', true);
    request.send();
}



function createKeys(text) {
    //    console.log(text);
    var patt1 = new RegExp("http");
    var patt2 = /\w+\W+\w+/;
    var patt3 = /\W(\W+)/;
    var patt4 = /\W/
    var keys = new Array();
    var f_words = text.split(" ");
    var words = new Array();
    for (var i = 0; i < f_words.length; i++) {
        if (patt3.test(f_words[i]) && !patt1.test(f_words[i])) {
            f_words[i] = f_words[i].split(patt3)[0];
            words.push(f_words[i]);
        }
        else if (patt2.test(f_words[i]) && !patt1.test(f_words[i])) {
            var temp = f_words[i].split(patt4);
            words.push(temp[0]);
            words.push(temp[1]);
        }
        else
            words.push(f_words[i]);

    }
    for (var i = 0; i < words.length; i++) {
        if (words[i].length > 3 && words[i].substr(0, 1) != "#" && words[i].substr(0, 1) != "@" && !patt1.test(words[i])) {
            keys.push(words[i])
        }
        for (var k = 0; k < keys.length; k++) {
            keys[k] = keys[k].toLowerCase();
        }
    }
    return returnKeys(keys);
}
/**
 * returns Twitter Keys
 * @param {type} keys
 * @returns {jqXHR}
 */
function returnKeys(keys) {
    return $.ajax({
        url: 'http://people.ischool.berkeley.edu/~chrisfan/twitter/keys.php',
        type: "POST",
        dataType: "json",
        data:
                { 'jsonkey': keys },
        success: function (data) {
            //            console.log(data);
        },
        error: function (data) {

        }
    });
}