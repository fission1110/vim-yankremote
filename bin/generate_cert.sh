#!/bin/bash
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
BOLD="\e[1m"
RESET="\e[0m"

echo -e $GREEN'Cleaning up old certificates'$RESET
rm server/server.cert 2>/dev/null
rm server/server.key 2>/dev/null

rm client/client.cert 2>/dev/null
rm client/client.key 2>/dev/null
rm client/client.csr 2>/dev/null

echo -e $GREEN'Generating server certificate.'$RESET
openssl req -subj '/CN=server/O=NA/C=US/ST=Utah/L=Draper' -nodes -out server/server.cert -newkey rsa:2048 -x509 -keyout server/server.key

# Copyt the server certificate to the client directory
cp server/server.cert client/server.cert

echo -e $GREEN'Generating Client certificate signing request.'$RESET
openssl req -new -subj '/CN=client/O=NA/C=US/ST=Utah/L=Draper' -nodes -out client/client.csr -newkey rsa:2048 -keyout client/client.key

echo -e $GREEN'Signing Client Certificate'$RESET
openssl x509 -req -days 365 -in client/client.csr -CA server/server.cert -CAkey server/server.key -set_serial 01 -out client/client.cert
