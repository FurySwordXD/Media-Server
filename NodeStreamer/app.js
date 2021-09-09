var express = require('express');
var streamer = require('./streamer')

var app = express();

app.get('/stream/:url', streamer.stream);

var port = 6969;
app.set('port', process.env.PORT || port);

app.listen(app.get('port'), function(){
    console.log('Server running on port ' + port);
});
