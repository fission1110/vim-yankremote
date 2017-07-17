if !has('python')
    " exit if python is not available.
    " XXX: raise an error message here
    finish
endif

python << EOL
import os
import socket, ssl
import vim
def PySendClipboard(line1,line2):
	# Get configuration from global vars
	ip = vim.eval('g:PasteSendIP')
	port = int(vim.eval('g:PasteSendPort'))
	cert = vim.eval('g:PasteSendCert')
	clientCert = vim.eval('g:PasteSendClientCert')
	clientKey = vim.eval('g:PasteSendClientKey')

	# Get the data from the current buffer range
	data = "\n".join(vim.current.buffer.range(int(line1), int(line2))[:])

	# Set the + register to the contents of the yanked text
	senclose = lambda str: "'"+str.replace("'", "''")+"'"
	vim.eval("setreg('@+', %s)" % (senclose(data)))

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
EOL

command -range PasteSend python PySendClipboard(<f-line1>,<f-line2>)
