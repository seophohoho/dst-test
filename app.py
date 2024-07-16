import socket
import threading
import time

from constants import DELETE_DATA, DELETE_QUERY, HOST, INSERT_DATA, INSERT_QUERY, SERVER_PORT
from utils import connect_db, execute_query, generate_hex

class JoaelectClient1:
    def __init__(self,server_host,server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_socket = None
        self.client_socket = None
        self.conn = connect_db()
        execute_query(self.conn,INSERT_QUERY,INSERT_DATA)
        self.start_listening()

    def start_listening(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.server_host, self.server_port))
            self.server_socket.listen(1)

            print(f"Listening on {self.server_host}:{self.server_port}")
            self.accept_server()
        except Exception as e:
            print(f"Failed to start server: {e}")
            self.stop_server()
    
    def accept_server(self):
        while True:
            try:
                self.client_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                #self.client_socket.sendall("CONNECT".encode('utf-8'))
                threading.Thread(target=self.receive_messages, daemon=True).start()
                threading.Thread(target=self.send_status, daemon=True).start()
                break
            except Exception as e:
                print(f"Error accepting client: {e}")
    
    def stop_server(self):
        if self.server_socket:
            self.server_socket.close()
        execute_query(self.conn,DELETE_QUERY,DELETE_DATA)
        print("Server stopped.")

    def receive_messages(self):
        while True:
            try:
                response = self.client_socket.recv(2048)
                if response:
                    addr = response.decode('utf-8').split('|')[0]   #상대편 측 주소
                    msg = response.decode('utf-8').split('|')[1]    #상대편 측 메시지
                    cmd = msg[2:4]                                  #상대편 메시지의 커맨드
                    print("Receive: "+msg+self.judge_cmd(cmd))
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
            self.disconnect()

    def send_status(self):
        while True:
            self.send_message(generate_hex(32))
            time.sleep(10)

    def judge_cmd(self,cmd):
        if cmd == "04":
            return "(Received a TimeSync request from the server.)"
        elif cmd == "21":
            self.send_ping()
            return "(Received a Ping request from the server.)"
            
    def send_ping(self):
        self.send_message(generate_hex(32))



if __name__ == "__main__":
    client1 = JoaelectClient1(HOST,SERVER_PORT)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client1.stop_server()
        print("Server stopped by user.")