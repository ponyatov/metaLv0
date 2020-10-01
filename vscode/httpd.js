
// powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest

var http = require('http');
http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Hello World\n');
}).listen(30000, "127.0.0.1");
console.log('Server running at http://127.0.0.1:30000/');