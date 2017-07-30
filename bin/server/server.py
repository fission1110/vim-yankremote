#!/usr/bin/env python3
import subprocess
import sys, os
import ssl
import signal
from distutils import spawn
try:
    from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler
except Exception as e:
    from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
try:
    import configparser
except Exception as e:
    import ConfigParser as configparser

#TODO: Make this a self watching daemon
dirPath = os.path.dirname(os.path.realpath(__file__))
configFile = dirPath + '/server.conf'

config = configparser.RawConfigParser()
config.read(configFile)

# TODO: make the binary configurable.
ip = config.get('server', 'listen_ip')
port = config.getint('server', 'listen_port')

# Paths are relative to the directory of the config file
confPath = os.path.dirname(configFile) + '/'
cert = confPath + config.get('server', 'server_cert')
privKey = confPath + config.get('server', 'server_key')

# TODO: Only xclip is tested
# TODO: would be nice if this tied directly into xlib and the windows API.
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
    print('Could not find a valid command in your path. Please install xclip, clip, xsel, or pbcopy')
    sys.exit(1)


class MySSL_ThreadingTCPServer(ThreadingMixIn, TCPServer):
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

        signal.signal(signal.SIGINT, self.handleClose)

    def handleClose(self, signum, frame):
        # for some reason self.shutdown() hangs?
        self.server_close()
        sys.exit()

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


class tcpHandler(StreamRequestHandler):
    def handle(self):
        data = bytes()
        blockSize = 4096
        while True:
            block = self.connection.recv(blockSize)
            data += block
            if len(block) < blockSize:
                break
        # TODO: would be cool if this was bi-directional
        # and the remote could ask for the server clipboard.
        # Then we could overwrite the put command in vim.
        self.sendToClipboard(data)

    def sendToClipboard(self, data):
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.communicate(input=data)

MySSL_ThreadingTCPServer((ip,port),tcpHandler,cert,privKey).serve_forever()
