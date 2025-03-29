import socket
import os


class Client:
    # server
    IP: str
    PORT: int

    client: socket.socket

    def __init__(self, addr, port=8721):
        # server
        self.PORT = port
        self.IP = addr

        # define socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.IP, self.PORT))
        except:
            print("err...")
            return

        while True:
            msg = self.client.recv(1024).decode()
            print(msg)

        self.client.close()