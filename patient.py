import socket
import ssl
import threading
from time import sleep
from config import Config


class Patient:
    def __init__(self, config: Config, port: int, id: int):
        self.id = id
        self.port = port
        self.config = config
        self.messages = []
        self.total_connected = 0
        self.msg_tag = f"({self.id} : {self.port})"

        threading.Thread(target=self.setup_connection).start()

    def setup_connection(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(self.config.cert_path)

        while True:
            try:
                socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                secured_conn = ctx.wrap_socket(socket_obj, server_hostname=self.config.hospital_ip)

                secured_conn.bind((self.config.hospital_ip, self.config.num_port + self.id))
                secured_conn.connect((self.config.hospital_ip, self.port))

                self.total_connected += 1
                self.secured_conn = secured_conn

                print(f"Successfully connected to {self.msg_tag}")

                return

            except socket.error:
                print(f"ERROR: Could not connect to {self.msg_tag}, will try again in 3 seconds")
                sleep(3)

    def get_message(self):
        while not self.messages:
            sleep(1)
        return self.messages.pop()

    def send_message(self, msg):
        self.secured_conn.sendall(msg.encode("utf-8"))

    def receive_message(self, conn: ssl.SSLSocket, addr):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(Config.cert_path, Config.p_key_path)
        sock = context.wrap_socket(conn, server_side=True)
        self.total_connected += 1

        while True:
            msg = sock.recv(1024)

            if len(msg) == 0:
                print(f"ERROR: Lost connection to {self.msg_tag}! Terminating process.")
                break

            self.messages.append(msg)

        sock.close()
        self.secured_conn.close()
        self.total_connected = 0
