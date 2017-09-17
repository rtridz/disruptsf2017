console.log("Starting server");

//Requirements
var Nexmo = require('nexmo');
var Express = require('express');
var MessagesManager = require('./messages_manager');

//Initialise the message manager
var msgManager = new MessagesManager();

//Initialise the nexmo client
var nexmo = new Nexmo({
    apiKey: 'df174b06',
    apiSecret: '6cbdba0099362623',
});

//Setup server to listen for messages
var app = Express();

app.get('/incoming-sms', function(req, res){
    res.sendStatus(200);

    msgManager.receiveMessage(req.query, sendMesssage);
});

//Function to send a text message
function sendMesssage(msg) {
    console.log("Sending: " + msg);
    nexmo.message.sendSms("12016728472", "14086097335", msg);
}

//Begin listening for messages
app.listen(80);
console.log("Listening for sms messages");

//temp
//sendMesssage('Hi, are you in need of assistance?');]=]]==]oi