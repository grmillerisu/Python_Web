var msgDict = {'messageStrings':[],'totalMessages':0,'finalString':""};

$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/messaging');

    socket.on('newmessage', function(msg){
       //console.log("Received " + msg.name + ": " + msg.str);
       var parse = false;
       var numMessages = occurrences(msgDict['finalString'],"<p>",false);
       if(msg.initMessage) {
          if (msg.totalMessages > numMessages) {
             var initMessageList = msg.msgList;
             var initLength = initMessageList.length;
             for(var i = 0; i < initLength; i++) {
                parseMessage(initMessageList[i]);
             }
             writeHtml();
          }
       } else {
          parse = true;
       }
       if(parse) {
          parseMessage(msg);
          writeHtml();
       }
    });
});

function writeHtml() {
   messageList = msgDict['messageStrings']
   numberOfMessages = messageList.length;
   var final_string = '';
   for (var i=0; i < numberOfMessages; i++) {
     final_string += messageList[i]['message_string'];
   }
   msgDict['finalString'] = final_string
   $('#log').html(final_string);
}

function parseMessage(msg) {
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
}

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


/** Function that count occurrences of a substring in a string;
 * @param {String} string               The string
 * @param {String} subString            The sub string to search for
 * @param {Boolean} [allowOverlapping]  Optional. (Default:false)
 *
 * @author Vitim.us https://gist.github.com/victornpb/7736865
 * @see Unit Test https://jsfiddle.net/Victornpb/5axuh96u/
 * @see http://stackoverflow.com/questions/4009756/how-to-count-string-occurrence-in-string/7924240#7924240
 */
function occurrences(string, subString, allowOverlapping) {

    string += "";
    subString += "";
    if (subString.length <= 0) return (string.length + 1);

    var n = 0,
        pos = 0,
        step = allowOverlapping ? 1 : subString.length;

    while (true) {
        pos = string.indexOf(subString, pos);
        if (pos >= 0) {
            ++n;
            pos += step;
        } else break;
    }
    return n;
}

function timer() {
    t = setTimeout(checkTimes, dt);
}
timer();
