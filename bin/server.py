#!/usr/bin/env python
from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler
import subprocess
import sys
import ssl
from distutils import spawn
try:
	import configparser
except Exception as e:
	import ConfigParser as configparser

configFile = './server.conf'

config = configparser.RawConfigParser()
config.read(configFile)

ip = config.get('server', 'listen_ip')
port = config.getint('server', 'listen_port')
cert = config.get('server', 'server_cert')
privKey = config.get('server', 'server_key')

possibleCommands = [
	('xclip', ['xclip', '-i', '-sel', 'c']),
	('clip', ['clip']),
	('xsel', ['xsel', '--clipboard', '--input']),
	('pbcopy', ['pbcopy'])
]

command = ''
for possibleCommand,arguments in possibleCommands:
	if spawn.find_executable(possibleCommand) != None:
		command = arguments
		break

if command == '':
	print 'Could not find a valid command in your path. Please install xclip, clip, xsel, or pbcopy'
	sys.exit(1)


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
