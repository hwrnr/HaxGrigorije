#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import subprocess
import time
import multiprocessing
import select
import sys
import json

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432      # Port to listen on (non-privileged ports are > 1023)

clients = {}

class ClientHandler(multiprocessing.Process):

    def __init__(self, clientsocket, address):
        multiprocessing.Process.__init__(self)
        self.clientsocket = clientsocket
        self.address = address

    def run(self):
        i = 0
        print("Connection started " + str(self.address))
        while True:
            data = self.clientsocket.recv(1024).decode("UTF-8")
            if not data:
                print("Connection interrupted " + str(self.address))
                break
            else:
                print(data)

    def execute(self, command):
        self.clientsocket.sendall(command.encode())

def acceptConnectionLoop():
    #da li ovde treba global clients ?
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind((HOST, PORT))
        serversocket.listen()

        while True:
            client, address = serversocket.accept()
            temp = ClientHandler(client, address)
            temp.start()
            clients[address[0]] = temp
            time.sleep(0.001)
            temp.execute('{"cmd": "files", "args": ["/"]}')

def main():
   acceptConnectionLoop()

if __name__ == "__main__":
    main()
