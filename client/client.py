import socket

class Client:
    # server
    IP: str
    PORT: int

    client: socket.socket

    def __init__(self, addr, port = 8721):
        # server
        self.PORT = port
        self.IP = addr

        # define socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.IP, self.PORT))

        msg = self.client.recv(1024)
        print("Received msg!")
        print(msg.decode())
        self.client.close();