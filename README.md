# vim YankRemote
A quick and dirty vim plugin to handle secure remote copying.

When I'm editing remotly, copy and paste becomes a burden. I have to disable line numbers, disable the mouse, then try to select the text in my terminal, and then copy from the terminal.

All the solutions online suggest turning on X11 forwarding in SSH in order to copy/paste into your local systems clipboard.
This doesn't work when you don't have X, and it seems silly to install X just for this.

Optionally you could use https://github.com/pocke/lemonade but their security model relies on attackers not knowing about arp spoofing.

My solution uses a tls socket to send the clipboard back to my local server, then uses xclip to shove that into my local system clipboard.
This utilizes tls client certificates for authentication so people on your lan can't just overwrite your clipboard with arbitrary data. Yay security.

## requires ##
* requires +python or +python3 support for vim on the remote server
* xclip (*untested* but may also work xsel(linux), pbcopy(mac), or clip(windows))
* openssl

## setup ##
The certificate setup can be a little daunting, but be brave, it's not as complex as it seems.
#### Server side setup
1. Generate a certificate and private key on your local host.
	* ``` $ cd ./bin; ./generate_cert.sh ```

2. Modify ./bin/server.config to change the settings. By default it binds to 0.0.0.0:9999

3. Start the clipboard server in the background.
	* ``` $ ./bin/server.py & disown```

4. Run the client test script and verify your clipboard was overwritten.
	* ``` cd ./bin; ./client_test.py ```
	* After that, your clipboard should contain Test Successful

#### Client side setup
5. Copy the server.cert, client.cert, and client.key over to the remote server.

6. Configure your .vimrc on the client to point back to your localhost as well as the full path to the cert

7. Start Yanking over tls!

## alternate setup ##
You could set up ssh port forwarding to push your local port 9999 to your remote server..
Then on the remote server, you could just connect to localhost:9999 and not have
to worry about firewalls.
``` $ ssh -R 9999:127.0.0.1:9999 user@host ```

## In your .vimrc
```
let g:PasteSendIP = '127.0.0.1' " The IP where server.py is running. Defaults to 127.0.0.1
let g:PasteSendPort = 9999 " The port server.py is running on. Defaults to 9999
let g:PasteSendCert = '/path/to/server.cert' " The full path of the certificate file. Defaults to <plugindir>/bin/server.cert
let g:PasteSendClientCert = '/path/to/client.cert' " The full path of the client certificate file. Defaults to <plugindir>/bin/client.cert
let g:PasteSendClientKey = '/path/to/client.key' " The full path of the client key file. Defaults to <plugindir>/bin/client.key

" Optionally you can overwrite the default yank keybinding completely
" nmap y <leader>y
" nmap yy <leader>yy
" xmap y <leader>y

" Or set your own keybindings and overwrite the defaults
" nmap <leader>x <Plug>PasteSend
" nmap <leader>xx <Plug>PasteSendLine
" xmap <leader>x <Plug>PasteSend
```
## Usage
Press <leader>yy to send the command to the remote server.
Press <leader>yiw to yank a word. Or any other vim idom
<leader>y also works in visual mode.

---

## Security Considerations
1. Be careful with your private keys.
2. It's generally bad practice to send private keys over the wire. It's better to copy your csr to the server, sign it, then copy the certificate back.
	* generate_cert.sh doesn't do this. I was lazy. It makes the instructions more complex.

