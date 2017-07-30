#!/usr/bin/env python

import os
import socket, ssl

try:
	import configparser
except Exception as e:
	import ConfigParser as configparser

configFile = './server.conf'

config = configparser.RawConfigParser()
config.read(configFile)

ip = config.get('client_test', 'ip')
port = config.getint('client_test', 'port')
cert = config.get('client_test', 'server_cert')
clientCert = config.get('client_test', 'client_cert')
clientKey = config.get('client_test', 'client_key')
data = config.get('client_test', 'test_message')

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
