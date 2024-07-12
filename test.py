import random
import socket
import threading
import time

from constants import *

def random_hex():
    return '{:02x}'.format(random.randint(0, 255))

def generate_hex(count):
    str_hex="FE"
    for i in range(count-2):
        str_hex+=random_hex()
    return str_hex+"FF"

class SetTopBox:
    def __init__(self, host, port, local_port=None):
        self.host = host
        self.port = port
        self.local_port = local_port
        self.socket = None
        self.connect()

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.local_port:
                self.socket.bind(('0.0.0.0', self.local_port))  # 로컬 포트를 바인딩
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            threading.Thread(target=self.receive_messages, daemon=True).start()
            threading.Thread(target=self.send_status, daemon=True).start()
        except Exception as e:
            print(f"Failed to connect: {e}")
            time.sleep(5)
            self.connect()

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode('utf-8'))
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Failed to send message: {e}")
            self.disconnect()

    def receive_messages(self):
        while True:
            try:
                response = self.socket.recv(1024)
                if response:
                    print(f"Received: {response.decode('utf-8')}")
                else:
                    self.disconnect()
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.disconnect()
                break

    def disconnect(self):
        print("Disconnected from server.")
        self.socket.close()
        self.connect()

    def close(self):
        self.socket.close()

    def send_status(self):
        while True:
            self.send_message(generate_hex(32))
            time.sleep(10)

    def request_time_data(self):
        self.send_message("FE093333333300FF")

    def send_ping_addr(self):
        self.send_message(generate_hex(32))

if __name__ == "__main__":
    client = SetTopBox(HOST, SERVER_PORT, LOCAL_PORT)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()
        print("Client closed")
