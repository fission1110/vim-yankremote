#!/usr/bin/env python3
import os, sys
import socket, ssl

try:
    import configparser
except Exception as e:
    import ConfigParser as configparser


dirPath = os.path.dirname(os.path.realpath(__file__)) + '/'
configFile = dirPath + 'client.conf'

config = configparser.RawConfigParser()
config.read(configFile)


ip = config.get('client', 'ip')
port = config.getint('client', 'port')

# Paths are relative to the directory of the config file
confPath = os.path.dirname(configFile) + '/'
cert = confPath + config.get('client', 'server_cert')
clientCert = confPath + config.get('client', 'client_cert')
clientKey = confPath + config.get('client', 'client_key')

# connect using ssl to the server
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
                           ca_certs=cert,
                           certfile=clientCert,
                           keyfile=clientKey,
                           cert_reqs=ssl.CERT_REQUIRED,
                           ssl_version=ssl.PROTOCOL_TLSv1)

ssl_sock.connect((ip,port))
ssl_sock.send(sys.stdin.read().encode())
ssl_sock.close()
