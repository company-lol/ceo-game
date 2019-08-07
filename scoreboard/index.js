var express = require('express');
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);

var scores = {}

let grab_scores = function(){
  const fs = require('fs');
  scores = []
  let rawdata = fs.readFileSync('data/scores.json');
  scores_obj = JSON.parse(rawdata)["_default"];
  console.log(scores_obj);
  const keys = Object.keys(scores_obj)
  console.log(keys)
  keys.forEach(element => {
    console.log(scores_obj[element])
    scores.push(scores_obj[element])
  });
  scores.sort((a, b) => (a.score > b.score) ? 1 : -1)
  console.log(scores)

  io.emit("scores",scores)
}


app.get('/', function(req, res){
  res.sendFile(__dirname + '/templates/index.html');

});


app.get('/game-end', function(req, res){
  grab_scores()
  
});




app.use(express.static("static"))
app.use(express.static("data"))



io.on('connection', function(socket){
  console.log('a user connected');
  grab_scores()
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
  });
});



http.listen(3000, function(){
  console.log('listening on *:3000');
});