var pos = require('pos');
var request = require('request');

module.exports = function () {

    var activeNumbers = {};

    //For reference: received message json format:
    /*

     { msisdn: '14086097335',
     to: '12016728472',
     messageId: '0B000000823A73DB',
     text: 'Yes, please send help',
     type: 'text',
     keyword: 'YES,',
     'message-timestamp': '2017-09-17 00:15:38' }

     */

    this.receiveMessage = function(newMessage, sendMesssage) {
        var number = newMessage.msisdn;

        if(number in activeNumbers){
            //Forward this message to the correct message handler
            activeNumbers[number].receiveMessage(newMessage, sendMesssage)
        }
        else{
            //Create new message handler
            var newUser = new UserSession(number);
            activeNumbers[number] = newUser;

            newUser.receiveMessage(newMessage, sendMesssage);
        }
    }

}

var conversationTree = require('./conversation_tree');

var UserSession = function (number) {
    this.number = number;
    this.messageHistory = [];
    this.tree = conversationTree;

    this.receiveMessage = function(newMessage, sendMesssage){
        this.messageHistory.push(newMessage);

        var messageText = newMessage.text;
        var response = "";

        //Parse within the conversation tree
        if(Object.keys(this.tree).length == 0){
            this.tree = conversationTree;
        }

        for(var m in this.tree){
            re = new RegExp(m.toLowerCase());
            if(re.test(messageText.toLowerCase())){
                response = this.tree[m]["response"];
                this.tree = this.tree[m]["tree"];
                break;
            }
        }

        if(response == "Help is on its way!"){
            extractLatitudeLongitude(messageText, function (position) {
                console.log(position);
                response = "http://maps.google.com/maps?q=" + position.lat + "," + position.lon + " be safe";
                sendMesssage(response);
            });
        }
        else{
            sendMesssage(response);
        }
    }
}

function extractLatitudeLongitude(text, extractionComplete) {
    text = text.toLowerCase();
    text = " " + text;
    text += " ";
    text = text.replace(" i'm ", "")
    var words = new pos.Lexer().lex(text);
    var tagger = new pos.Tagger();
    var taggedWords = tagger.tag(words);

    var address = "";
    for (i in taggedWords) {
        var taggedWord = taggedWords[i];
        var word = taggedWord[0];
        var tag = taggedWord[1];
        if(tag == "NN" || tag == "CD" || tag == "JJ"){
            address += word + " ";
        }
    }
    address = address.trim();
    request('http://open.mapquestapi.com/nominatim/v1/search.php?key=UShjaMayAC4UkuBJ5nu5rqFuraxzEOQU&format=json&q=' + address.replace(" ", "+") + '+usa&addressdetails=1&limit=3&viewbox=-1.99%2C52.02%2C0.78%2C50.94&exclude_place_ids=41697', function (error, response, body) {
        var jsonObject = JSON.parse(body);
        if(jsonObject){
            var lat = jsonObject[0].lat;
            var lon = jsonObject[0].lon;
            extractionComplete({"lat":lat, "lon":lon});
        }
    });
}