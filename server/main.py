from server import Server
from interface import Interface

if __name__ == "__main__":
    server = Server(address="0.0.0.0", port=8721)
    server.start()

    interface = Interface(server=server)
    interface.run()