import socket
from  import requestparser


HOST = "localhost"
PORT = 40419
end_of_stream = '\r\n\r\n'


def handle_client(connection):
    client_data = ''
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            client_data += data.decode()
            if end_of_stream in client_data:
                break
        http_response = requestparser(client_data)
        connection.send(http_response.encode())


def run_server():
    with socket.socket() as serverSocket:
        # Bind the tcp socket to an IP and port
        serverSocket.bind((HOST, PORT))
        # Keep listening
        print(f"Running server on {HOST}:{PORT}...")
        serverSocket.listen()

        while True:
            (clientConnection, clientAddress) = serverSocket.accept()
            handle_client(clientConnection)
            print(f"Sent data to {clientAddress}")


if __name__ == "__main__":
    run_server()

