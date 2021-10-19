import socket


class ConnectionSocket:
    def __init__(self, host: tuple):
        self.host_ip = host[0]
        self.host_port = host[1]

        self.start_connection()

    def start_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket = s

        s.connect((self.host_ip, self.host_port))

    def send_message(self, message: str, app):
        try:
            with app.app_context():
                self.socket.sendall(message.encode('utf-8'))

                self.socket.recv(1024)
        except socket.error:
            print("connection failed, maybe server is down?")
