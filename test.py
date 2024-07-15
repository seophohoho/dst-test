import socket
import threading
import time

from constants import DELETE_DATA, DELETE_QUERY, INSERT_DATA, INSERT_QUERY
from utils import connect_db, generate_hex

class SetTopBoxServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.conn = connect_db()
        self.start_server()

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print(f"Listening on {self.host}:{self.port}")
            insert_sync(self.conn)
            self.accept_client()
        except Exception as e:
            print(f"Failed to start server: {e}")
            self.stop_server()

    def accept_client(self):
        while True:
            try:
                self.client_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                self.client_socket.sendall("CONNECT".encode('utf-8'))
                threading.Thread(target=self.receive_messages, daemon=True).start()
                break
            except Exception as e:
                print(f"Error accepting client: {e}")

    def receive_messages(self):
        while True:
            try:
                response = self.client_socket.recv(1024)
                if response:
                    print(f"Received: {response.decode('utf-8')}")
                else:
                    self.disconnect_client()
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.disconnect_client()
                break

    def disconnect_client(self):
        print("Client disconnected.")
        if self.client_socket:
            self.client_socket.close()
        self.client_socket = None
        self.accept_client()

    def stop_server(self):
        if self.server_socket:
            self.server_socket.close()
        delete_sync(self.conn)
        print("Server stopped.")
    
    def send_message(self, message):
        try:
            self.server_socket.sendall(message.encode('utf-8'))
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Failed to send message: {e}")
            self.disconnect()

    def send_status(self):
        while True:
            self.send_message(generate_hex(32))
            time.sleep(10)

if __name__ == "__main__":
    server = SetTopBoxServer("192.168.0.8", 43001)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop_server()
        print("Server stopped by user.")
