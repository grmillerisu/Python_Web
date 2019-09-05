var msgDict = {'messageStrings':[]};

$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/messaging');
    var msgNames = [];

    socket.on('newmessage', function(msg){
       console.log("Received " + msg.name + ": " + msg.str);
       if (!msgNames.includes(msg.name)) {
          msgNames.push(msg.name);
       }
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
          msgDict[messageTitleKey] = "<h4 id=\"latest_" + msg.name + "\">" + msg.name + '. age = 0.0 s</h4>';
       }
       msgDict[messagesKey].push(msg.str);
       var message_string = "<div id=\"" + msg.name + "\">\n";
       message_string += msgDict[messageTitleKey];
       for (var i = msgDict[messagesKey].length -1; i >= 0; i--){

           if (i == msgDict[messagesKey].length -1) {
             //message_string +=  "<p id=\"latest_" + msg.name + "\">" + msgDict[messagesKey][i];
             message_string +=  "<p>" + msgDict[messagesKey][i];
             message_string +=  ". Latest message";
          } else {
             message_string += "<p> " + msgDict[messagesKey][i];
          }
           message_string += "</p>"
       }
       message_string += "\n</div>";
       var messageList = msgDict['messageStrings']
       var numberOfMessages = messageList.length;
       var found = false;
       if (numberOfMessages > 0) {
          for (var i=0; i < numberOfMessages; i++) {
             currentMessageDict = messageList[i];
             if (currentMessageDict['name'] == msg.name) {
                currentMessageDict['message_string'] = message_string;
                currentMessageDict['age'] = 0.0;
                found = true;
                break;
             }
          }
       }
       if (!found) {
          var thisMessageDict = {'name':msg.name,'message_string':message_string,'age':0.0};
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
});

var dt = 100;

function checkTimes() {
   var messageList = msgDict['messageStrings']
   var numberOfMessages = messageList.length;
   if (numberOfMessages > 0) {
      for (var i = 0; i < numberOfMessages; i++) {
         var messageDict = messageList[i];
         var dt_s = dt / 1000.0;
         messageDict['age'] += dt_s;
         var newestMsgHtml = document.getElementById("latest_" +messageDict['name']);
         var oldText = newestMsgHtml.innerText;
         var withoutAge = oldText.split(". age")[0]
         var withAge = withoutAge + ". age = " + messageDict['age'].toFixed(1).toString() + " s.";
         newestMsgHtml.innerText = withAge;
      }
   }
   timer();
}

function timer() {
    t = setTimeout(checkTimes, dt);
}
timer();
