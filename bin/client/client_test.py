#!/usr/bin/env python3
import os, sys
import socket, ssl

try:
    import configparser
except Exception as e:
    # Python2 calls configparser ConfigParser
    import ConfigParser as configparser

# TODO: A verbose mode would be nice..
# we could test that the certificate file is readable
# Validate the port/ip
# We could test that the client and server certificate verify successfully
# - need to find the python ssl api equivelent of openssl verify -purpose sslclient  -CAfile ./server.cert ./client.cert
# Test the tcp connection to the server
# Test the tls connection to the server



dirPath = os.path.dirname(os.path.realpath(__file__))
configFile = dirPath + '/client.conf'

config = configparser.RawConfigParser()
config.read(configFile)

ip = config.get('client', 'ip')
port = config.getint('client', 'port')

# Paths are relative to the directory of the config file
confPath = os.path.dirname(configFile) + '/'
cert = confPath + config.get('client', 'server_cert')
clientCert = confPath + config.get('client', 'client_cert')
clientKey = confPath + config.get('client', 'client_key')

if not os.path.isfile(cert):
    print('Error: Cert file %s doesn\'t exist.' % (cert))
    sys.exit(1)

if not os.path.isfile(clientCert):
    print('Error: Cert file %s doesn\'t exist.' % (clientCert))
    sys.exit(1)

if not os.path.isfile(clientKey):
    print('Error: Key file %s doesn\'t exist.' % (clientKey))
    sys.exit(1)

data = config.get('client', 'test_message')

# connect using ssl to the server
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
                           ca_certs=cert,
                           certfile=clientCert,
                           keyfile=clientKey,
                           cert_reqs=ssl.CERT_REQUIRED,
                           ssl_version=ssl.PROTOCOL_TLSv1)

try:
    ssl_sock.connect((ip,port))
except ConnectionRefusedError as e:
    print('%s: Is the server running? Is a firewall blocking the connection?' % (e))
    sys.exit(1)

ssl_sock.send(data.encode())
ssl_sock.close()
print('Your clipboard should now contain:' + data)
