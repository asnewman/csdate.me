'use strict';

const common = require('../common');
const assert = require('assert');
const net = require('net');

const server = net.createServer(handle);

const N = 100;
const buf = Buffer('aa');

server.listen(common.PORT, function() {
  const conn = net.connect(common.PORT);

  conn.on('connect', () => {
    let res = true;
    let i = 0;
    for (; i < N && res; i++) {
      conn.cork();
      conn.write(buf);
      res = conn.write(buf);
      conn.uncork();
    }
    assert.equal(i, N);
    conn.end();
  });
});

process.on('exit', function() {
  assert.equal(server.connections, 0);
});

function handle(socket) {
  socket.resume();

  socket.on('error', function(err) {
    socket.destroy();
  }).on('close', function() {
    server.close();
  });
}
