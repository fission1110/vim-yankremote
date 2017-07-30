#!/usr/bin/env python

import os
import socket, ssl
import vim

def PySendClipboard():
	# Get configuration from global vars
	ip = vim.eval('g:PasteSendIP')
	port = int(vim.eval('g:PasteSendPort'))
	cert = vim.eval('g:PasteSendCert')
	clientCert = vim.eval('g:PasteSendClientCert')
	clientKey = vim.eval('g:PasteSendClientKey')

	data = vim.eval('@@')

	# connect using ssl to the server
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ssl_sock = ssl.wrap_socket(s,
							   ca_certs=cert,
							   certfile=clientCert,
							   keyfile=clientKey,
							   cert_reqs=ssl.CERT_REQUIRED,
							   ssl_version=ssl.PROTOCOL_TLSv1)

	ssl_sock.connect((ip,port))
	ssl_sock.send(bytes(data, 'utf-8'))
	ssl_sock.close()
