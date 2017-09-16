console.log("Hello");

//Requirements
var Nexmo = require('nexmo');

//Initialise the nexmo client
var nexmo = new Nexmo({
    apiKey: 'df174b06',
    apiSecret: '6cbdba0099362623',
});

//Begin listening for text messages
var Express = require('express');

var app = Express();

app.get('/incoming-sms', function(req, res){
    console.log(req.query.text);
    res.sendStatus(200);
});

app.get('/', function(req, res){
    res.sendStatus(200);
});

app.listen(80);

//Function to send a text message
function sendMesssage(msg) {
    nexmo.message.sendSms("12016728472", "14086097335", msg);
}

//sendMesssage('Hi, are you in need of assistance?');

console.log("Goodbye");