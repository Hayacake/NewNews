#! /usr/bin/python3
# sendCliant.py - send json data to cliant

import socket



IP_ADDRESS = "133.242.175.169"
PORT = "56747"



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP_ADDRESS, PORT))  # IPとポート番号を指定します
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Welcome to the server!", 'utf-8'))
    clientsocket.close()