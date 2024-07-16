import socket
import threading
import time
from constants import DELETE_DATA, DELETE_QUERY, HOST, INSERT_DATA, INSERT_QUERY, SERVER_PORT
from utils import connect_db, execute_query, generate_hex

class JoaelectClient1:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = None
        self.conn = connect_db()
        execute_query(self.conn, INSERT_QUERY, INSERT_DATA)
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_host, self.server_port))
            print(f"Connected to Netty server at {self.server_host}:{self.server_port}")
            self.client_socket.sendall("CONNECT".encode('utf-8'))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            threading.Thread(target=self.send_status, daemon=True).start()
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.stop_client()

    def stop_client(self):
        if self.client_socket:
            self.client_socket.close()
        execute_query(self.conn, DELETE_QUERY, DELETE_DATA)
        print("Client stopped.")

    def receive_messages(self):
        while True:
            try:
                response = self.client_socket.recv(1024)
                if response:
                    addr = response.decode('utf-8').split('|')[0]  # 상대편 측 주소
                    msg = response.decode('utf-8').split('|')[1]   # 상대편 측 메시지
                    cmd = msg[2:4]                                 # 상대편 메시지의 커맨드
                    print("Receive: " + msg + self.judge_cmd(cmd))
                else:
                    self.disconnect_client()
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.disconnect_client()
                break

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode('utf-8'))
            print(f"Send: {message}")
        except Exception as e:
            print(f"Failed to send message: {e}")
            self.disconnect_client()

    def send_status(self):
        while True:
            self.send_message(generate_hex(32))
            time.sleep(10)

    def judge_cmd(self, cmd):
        if cmd == "04":
            return "(Received a TimeSync request from the server.)"
        elif cmd == "21":
            self.send_ping()
            return "(Received a Ping request from the server)"

    def send_ping(self):
        self.send_message(generate_hex(32))

    def disconnect_client(self):
        print("Disconnected from server.")
        self.client_socket.close()
        self.connect_to_server()

if __name__ == "__main__":
    client1 = JoaelectClient1(HOST, SERVER_PORT)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client1.stop_client()
        print("Client stopped by user.")
