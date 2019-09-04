
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/messaging');

    var msgDict = {'messageStrings':[]};

    socket.on('newmessage', function(msg){
       console.log("Received " + msg.name + ": " + msg.str);
       var msgLength = msg.length;
       var messagesKey = msg.name + '_msgs';
       var maxLengthKey = msg.name + '_Maxlen';
       var messageTitleKey = msg.name + '_Title';
       if (maxLengthKey in msgDict) {
          if (msgDict[messagesKey].length >= msgDict[maxLengthKey]) {
             msgDict[messagesKey].shift();
          }
       } else {
          msgDict[maxLengthKey] = msg.length;
          msgDict[messagesKey] = [];
          msgDict[messageTitleKey] = '<h3>' + msg.name + '</h3>';
       }
       msgDict[messagesKey].push(msg.str);
       var message_string = msgDict[messageTitleKey];
       for (var i = 0; i < msgDict[messagesKey].length; i++){
           message_string = message_string + '<p>' + msgDict[messagesKey][i] + '</p>';
       }
       var messageList = msgDict['messageStrings']
       var numberOfMessages = messageList.length;
       var found = false;
       if (numberOfMessages > 0) {
          for (var i=0; i < numberOfMessages; i++) {
             currentMessageDict = messageList[i];
             if (currentMessageDict['name'] == msg.name) {
                currentMessageDict['message_string'] = message_string;
                found = true;
                break;
             }
          }
       }
       if (!found) {
          var thisMessageDict = {'name':msg.name,'message_string':message_string};
          msgDict['messageStrings'].push(thisMessageDict);
       }
       messageList = msgDict['messageStrings']
       numberOfMessages = messageList.length;
       var final_string = '';
       for (var i=0; i < numberOfMessages; i++) {
         final_string += messageList[i]['message_string'];
       }
       $('#log').html(final_string);
    });
    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        }
        $('#log').html(numbers_string);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p>' + (numbers_received[i]+1).toString() + '</p>';
        }
        $('#log2').html(numbers_string);
    });

});
