var express = require('express');
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

var scores = {}

let grab_scores = function(){
  const fs = require('fs');
  scores = []
  let rawdata = fs.readFileSync('data/scores.json');
  scores_obj = JSON.parse(rawdata)["_default"];
  
  const keys = Object.keys(scores_obj)
  
  keys.forEach(element => {
    
    scores.push(scores_obj[element])
  });
  scores.sort((a, b) => (a.score > b.score) ? 1 : -1)
  

  io.emit("scores",scores)
}


app.get('/', function(req, res){
  res.sendFile(__dirname + '/templates/index.html');
});


app.post('/game-end', function(req, res){
  
  console.log("Emit recent time: "+ req.body.time)
  io.emit("recent_time",req.body.time)
  res.end()
});


app.use(express.static("static"))
app.use(express.static("data"))



io.on('connection', function(socket){
  
  grab_scores()
  socket.on('disconnect', function(){
    
  });

  socket.on('refreshScores', function(msg){
    grab_scores()
  });

});



http.listen(3000, function(){
  console.log('listening on *:3000');
});