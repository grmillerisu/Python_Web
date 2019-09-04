
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    var arrayLength = msg_var.length;
    for(var i = 0; i < arrayLength; i++) {
      message = msg_var[i];
      socket.on(message['name'], function(msg) {
         console.log("Received " + message['name'] + msg.number);
         var str = '<p>' + msg.number.toString() + '</p>';
         $('#'+message['name']+'_log').html(str);
      });
   }
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
