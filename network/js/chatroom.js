//$(document).ready=(function(){
alert("helloworld");
var socket=new WebSocket('ws://192.168.1.134:5000');
socket.onopen=function(event){
    socket.send('login:1,username:jiu,password:123456')
    socket.onmessage=function(event){
        console.log("client received a message",event);
    }
    socket.onclose=function(event){
        console.log("Cilent notified socket has closed",event);
    }
};
//})
