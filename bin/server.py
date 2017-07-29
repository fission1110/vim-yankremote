#!/usr/bin/env python
from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler
import subprocess
import ssl
from distutils import spawn

ip = '0.0.0.0'
port = 9999
cert = './server.cert'
privKey = './server.key'

possibleCommands = [
	('xclip', ['xclip', '-i', '-sel', 'c']),
	('clip', ['clip']),
	('xsel', ['xsel', '--clipboard', '--input']),
	('pbcopy', ['pbcopy'])
]

for possibleCommand,arguments in possibleCommands:
	if spawn.find_executable(possibleCommand) != None:
		command = arguments
		break

class MySSL_TCPServer(TCPServer):
    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 certfile,
                 keyfile,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 cert_reqs= ssl.CERT_REQUIRED,
                                 certfile = self.certfile,
                                 keyfile = self.keyfile,
                                 ca_certs=self.certfile,
                                 ssl_version = self.ssl_version)
        return connstream, fromaddr

class MySSL_ThreadingTCPServer(ThreadingMixIn, MySSL_TCPServer): pass

class tcpHandler(StreamRequestHandler):

    def handle(self):
        data = ''
        blockSize = 4096
        while True:
            block = self.connection.recv(blockSize)
            data += block
            if len(block) < blockSize:
                break
        self.sendToClipboard(data)

    def sendToClipboard(self, data):
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.communicate(input=data)

MySSL_ThreadingTCPServer((ip,port),tcpHandler,cert,privKey).serve_forever()
