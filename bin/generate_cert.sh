echo 'Generating server certificate.'
openssl req -subj '/CN=server/O=NA/C=US/ST=Utah/L=Draper' -nodes -out server.cert -newkey rsa:2048 -x509 -keyout server.key

echo 'Generating Client certificate signing request.'
openssl req -new -subj '/CN=client/O=NA/C=US/ST=Utah/L=Draper' -nodes -out client.csr -newkey rsa:2048 -keyout client.key

echo 'Signing Client Certificate'
openssl x509 -req -days 365 -in ./client.csr -CA server.cert -CAkey server.key -set_serial 01 -out client.cert

# Why keep the client.csr around?
rm ./client.csr
