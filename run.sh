#!/bin/bash
CERT=""
HOST="127.0.0.1"
while (( "$#" )); do
  case $1 in
    -host) HOST=$2;;
    -cert) CERT=$2;;
  esac
  shift
done

echo $CERT
echo $HOST

export FLASK_DEBUG=1
export FLASK_APP=gpa_server.py
export FLASK_RUN_PORT=8000
if [ -z "$CERT" ]
	then
		flask run --host $HOST
	else
		flask run --host $HOST --cert $CERT/cert.pem --key $CERT/key.pem
fi
