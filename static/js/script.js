/*
    Sample script.js JavaScript file

    Author: Mike Dory
    11.12.11, updated 11.24.12
*/


// your fancy JS code goes here!

$(document).ready(function() { 
	document.session = $('#session').val();
	
	setTimeout(getTweet, 1000);
});


function getTweet() {
	console.log("in here");
	var host = 'ws://localhost:8000/ws';
	var websocket = new WebSocket(host);
	websocket.onopen = function (evt) { };
	websocket.onmessage = function(evt) {
		console.log($.parseJSON(evt.data)['tweet_text'])
		$('.tweet').html($.parseJSON(evt.data)['tweet_text']); 
	};
	websocket.onerror = function (evt) { };
}

















