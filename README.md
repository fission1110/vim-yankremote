# vim YankRemote
A quick and dirty vim plugin to handle remote copy/paste.

When I'm editing remotly, copy and paste becomes a burden. I have to disable line numbers, disable the mouse, then try to select the text in my terminal, and then copy from the terminal.

All the solutions online suggest turning on X11 forwarding in SSH in order to copy/paste into your local systems clipboard.
This doesn't work when you don't have X, and it seems silly to install X just for this.

My solution uses a tls socket to send the clipboard back to my local server, then uses xclip to shove that into my local system clipboard.
This utilizes tls client certificates for authentication so people on your lan can't just overwrite your clipboard with arbitrary data. Yay security.

## requires ##
* requires +python or +python3 support for vim on the remote server
* xclip (*untested* xsel(linux), pbcopy(mac), or clip(windows))
* openssl

## setup ##
1. Generate a certificate and private key on your local host.
	* ``` $ cd ./bin; ./generate_cert.sh ```
2. Modify server.py to change the settings. By default it binds to 0.0.0.0:9999
3. Start the clipboard server.
	* ``` $ cd ./bin; ./server.py & ```
4. Copy the server.cert, client.cert, and client.key over to the remote server.
5. Configure your .vimrc to point back to your local host, with the full path of the cert
6. Start Yanking over tls!

## alternate setup ##
You could set up ssh port forwarding to push your local port 9999 to your remote server..
Then on the remote server, you could just connect to localhost:9999 and not have
to worry about firewalls.

## In your .vimrc
```
let g:PasteSendIP = '127.0.0.1' " The IP where server.py is running. Defaults to 127.0.0.1
let g:PasteSendPort = 9999 " The port server.py is running on. Defaults to 9999
let g:PasteSendCert = '/path/to/server.cert' " The full path of the certificate file. Defaults to <plugindir>/bin/server.cert
let g:PasteSendClientCert = '/path/to/client.cert' " The full path of the client certificate file. Defaults to <plugindir>/bin/client.cert
let g:PasteSendClientKey = '/path/to/client.key' " The full path of the client key file. Defaults to <plugindir>/bin/client.key
vmap <leader>y :PasteSend<cr> " Optionally you can overwrite visual yank
```
## Usage
This plugin creates the PasteSend command.

---

Send your selection with
``` :'<,'>PasteSend ```

or send the entire file with
``` :%PasteSend ```

---

See ```:help range```

## Security Considerations
1. Be careful with your private keys. With those, someone could connect to your server and overwrite the clipboard. This is extremely dangerous.
	* It's generally bad practice to send private keys over the wire. It's better to copy your csr to the server, sign it, then copy the certificate back. generate_cert.sh doesn't do this.
2. tls common name verification is not on. By default, your common name is 'server' for the CA/Server Cert, and 'client' for the client cert.
3. Don't put this on the public internet.. keep it behind your vpn/firewall..
