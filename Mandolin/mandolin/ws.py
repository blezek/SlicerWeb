"""
import mandolin.ws
reload(mandolin.ws); ss = mandolin.ws.WServer()
"""

import logging
logger = logging.getLogger('ws')
logger.setLevel(logging.DEBUG)

from collections import deque
from __main__ import qt

import sys
import base64
from hashlib import sha1
WS_KEY = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


handshake = '\
HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Version: 13\r\n\
WebSocket-Origin: http://localhost:8888\r\n\
WebSocket-Location: ws://localhost:9999/\r\n\
'


class WServer:
  def __init__(self):
    import socket
    # self.sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = qt.QTcpServer()
    self.server.listen(qt.QHostAddress("0.0.0.0"),9999)
    self.server.connect('newConnection()', self.handleConnect)

  def handleConnect(self):
    logger.debug("Got connection")
    socket = self.server.nextPendingConnection()
    logger.debug("Got connection from {}".format(socket.peerName()))
    self.ws = WS(socket)

  def close(self):
    self.ws.close();
    self.server.close()
 
class WS:
  def __init__(self, socket):
    self.handshaken = False 
    self.data = ''
    self.header = ''
    self.sock = socket
    self.send_buffer = deque()
    self.sock.connect('readyRead()', self.handleRead)

 
  def close(self):
    self.sock.close();

  def handleWrite(self,fd):
    logger.debug ( "Sending data: {}".format(len(self.send_buffer)))
    while len(self.send_buffer):
      self.sock.sendall(self.send_buffer.popleft())

  def handleRead(self):
    tmp = self.sock.read(1024)
    logger.info("handleRead read {} bytes".format(tmp.size()))
    if tmp.size() == 0:
      logger.debug("Got zero bytes, closing")
      self.close()
      return

    tmp = str(tmp)
    if self.handshaken == False:
      self.header += tmp
      logger.debug ( "Looking for handshake\nheader: {}".format(self.header))
      if self.header.find('\r\n\r\n') != -1:
        self.data = self.header.split('\r\n\r\n', 1)[1]
        h = self.header.split('\r\n\r\n', 1)[0]
        s = h.split("\r\n")
        self.headers = dict(item.split(": ") for item in s[1:])
        self.handshaken = True
        key = self.headers.get('Sec-WebSocket-Key')
        if key:
          ws_key = base64.b64decode(key.encode('utf-8'))
        secret = base64.b64encode(sha1(key.encode('utf-8') + WS_KEY).digest())
        self.sock.write(handshake + 'Sec-WebSocket-Accept: ' + secret + '\r\n\r\n')
        logger.debug("Got handshake \nheaders: {}".format(self.headers))
    else:
      self.data += tmp;
      validated = []
      msgs = self.data.split('\xff')
      self.data = msgs.pop()
      for msg in msgs:
        if msg[0] == '\x00':
          validated.append(msg[1:])
 
      for v in validated:
        logger.debug("Got message: {}".format(v))
        self.send_buffer.append('\x00' + v + '\xff')
        self.sock.write('\x00' + v + '\xff')


# while True:
#     if handshaken == False:
#         header += client.recv(16)
#         if header.find('\r\n\r\n') != -1:
#             data = header.split('\r\n\r\n', 1)[1]
#             handshaken = True
#             client.send(handshake)
#     else:
#             tmp = client.recv(128)
#             data += tmp;
 
#             validated = []
 
#             msgs = data.split('\xff')
#             data = msgs.pop()
 
#             for msg in msgs:
#                 if msg[0] == '\x00':
#                     validated.append(msg[1:])
 
#             for v in validated:
#                 print v
#                 client.send('\x00' + v + '\xff')
