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
        var number = newMessage.msisdn;

        if(number in activeNumbers){
            //Forward this message to the correct message handler
            return activeNumbers[number].receiveMessage(newMessage)
        }
        else{
            //Create new message handler
            var newUser = new UserSession(number);
            activeNumbers[number] = newUser;

            return newUser.receiveMessage(newMessage);
        }
    }

}

var conversationTree = require('./conversation_tree');

var UserSession = function (number) {
    this.number = number;
    this.messageHistory = [];
    this.tree = conversationTree;

    this.receiveMessage = function(newMessage){
        this.messageHistory.push(newMessage);

        var response = "";

        //Parse within the conversation tree
        for(var m in this.tree){
            re = new RegExp(m.toLowerCase());
            if(re.test(newMessage.text.toLowerCase())){
                response = this.tree[m]["response"];
                this.tree = this.tree[m]["tree"];
            }
        }

        if(Object.keys(this.tree).length == 0){
            this.tree = conversationTree;
        }

        return response;
    }
}