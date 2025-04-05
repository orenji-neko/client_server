from server import Server

if __name__ == "__main__":
    server = Server(address="0.0.0.0", port=8721);
    server.listen();