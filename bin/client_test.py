#!/usr/bin/env python

import os
import socket, ssl

ip = '127.0.0.1'
port = 9999
cert = './server.cert'
clientCert = './client.cert'
clientKey = './client.key'

data = 'Test Successful'

# connect using ssl to the server
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
						   ca_certs=cert,
						   certfile=clientCert,
						   keyfile=clientKey,
						   cert_reqs=ssl.CERT_REQUIRED,
						   ssl_version=ssl.PROTOCOL_TLSv1)

ssl_sock.connect((ip,port))
ssl_sock.send(data)
ssl_sock.close()
print 'Your clipboard should now contain:' + data
