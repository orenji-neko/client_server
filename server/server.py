from operator import add
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, main_thread

class Connection:
    address: str
    connection: socket

    def __init__(self, address: str, connection: socket):
        self.address = address
        self.connection = connection

class Server:
    IP: str
    PORT: int
    server: socket
    connections: list[Connection]

    def __init__(self, address: str, port=8721):
        self.connections = []

        self.PORT = port
        self.ADDRESS = address

        # define socket
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.ADDRESS, self.PORT))

    # This server handles connections
    # between multiple clients using 
    # multithreading.
    def listen(self):
        # This thread handles accepting 
        # connections from multiple clients.
        main_thread = Thread(target=self._main_thread, name="main_thread")
        main_thread.start()

    # Main Thread
    def _main_thread(self):
        self.server.listen(5)
        print(f"Listening at port {self.PORT}...")

        while(True):
            con, addr = self.server.accept()
            print(f"Established connection to {addr[0]}...")
            # Add accepted connection to connections list.
            self.connections.append(Connection(address=addr[0], connection=con))

    # Get connection list
    def get_connections(self):
        return self.connections