import socket


class Server:
    IP: str
    PORT: int
    server: socket.socket

    def __init__(self, port=8721):
        self.PORT = port
        # public
        self.IP = "0.0.0.0"

        # define socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind((self.IP, self.PORT))
        self.server.listen(5)
        print("listening for connections...")

        # client
        client_con, client_addr = self.server.accept((self.IP, self.PORT))
        
        while(True):
            msg = input()
            client_con.send(msg.encode())

        client_con.close()
