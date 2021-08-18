import socket


class ConnectionSocket():
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port

        self.start_connection()

    def start_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket = s

        s.connect((self.host_ip, self.host_port))

    def send_message(self, message: str):
        self.socket.sendall(message.encode('utf-8'))

        self.socket.recv(1024)
