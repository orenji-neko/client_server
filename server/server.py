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

    # Threads
    main_thread: Thread
    con_threads: list[Thread]

    def __init__(self, address: str, port=8721):
        self.connections = []
        self.con_threads = []

        self.PORT = port
        self.ADDRESS = address

        # define socket
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.ADDRESS, self.PORT))

    # This server handles connections
    # between multiple clients using 
    # multithreading.
    def start(self):
        # This thread handles accepting 
        # connections from multiple clients.
        self.main_thread = Thread(target=self._main_thread, name="main_thread")
        self.main_thread.start()

    # Main Thread
    def _main_thread(self):
        self.server.listen(5)

        while(True):
            con, addr = self.server.accept()
            # Add accepted connection to connections list.
            new_connection = Connection(address=addr[0], connection=con)
            self.connections.append(new_connection)
            # create connection thread
            self.con_threads = Thread(target=self._con_thread(new_connection))

    # Connection thread
    def _con_thread(self, connection: Connection):
        while(True):
            out = connection.connection.recv(1024).decode()
            print(f"\nOUT [{connection.address}] - {out}")

    # Get connection list
    def get_connections(self):
        return self.connections