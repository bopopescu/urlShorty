/**
    Tiffany just copy and paste this code into your js.

    The toplevel webpage needes to added the references to the scrpit files. Look template/twitter_tutorial.html
    	<script type="text/javascript" src="static/js/Twitter/twitterAPI.js"></script>
		<script type="text/javascript" src="static/js/Twitter/recommendationScript.js"></script>
		<script type="text/javascript" src="static/js/Twitter/rankFunction.js"></script>
        <script type="text/javascript" src="static/js/twitter_example.js"></script>
**/
$(document).ready(function () {
    console.log("Ready");
    
    //getURLHeadInfo(temp);

    $("#tweet-tag-suggest").click(function () {
        var text = $("#tweet-text").val();
	
        console.log("URLShorty suggestions for url:", text);        
        getURLHeadInfo(text).done(function (data) {
			if(data.keywords){
				console.log("Keywords Retrieved", data.keywords);
			}
			rankFunction(data.title).then(function (stuff) {
			    //console.log("does this work???????????????????????????????", stuff);
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

function putinDom(words_list) {
    console.log("Inside the DOM function", words_list);
    for (var counter = 0; counter < words_list.length; counter++) {
        console.log("Generate Cllick Event and Put in DOM: ", words_list[counter]);
    }

}
