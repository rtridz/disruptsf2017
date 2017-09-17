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

    this.receiveMessage = function(newMessage) {
        var number = newMessage.to;

        if(number in activeNumbers){
            //Forward this message to the correct message handler
            activeNumbers[number].receiveMessage(newMessage)
        }
        else{
            //Create new message handler
            var newUser = new UserSession(number);
            newUser.receiveMessage(newMessage);
            activeNumbers[number] = newUser;
        }
    }

}

var UserSession = function (number) {
    this.number = number;
    this.messageHistory = [];
    console.log("New number!")

    this.receiveMessage = function(newMessage){
        console.log("message received")
        this.messageHistory.push(newMessage);
    }
}