import socket
import ssl
import threading
from time import sleep
from config import Config


class Patient:
    def __init__(self, config, port, id):
        self.conn = []
        self.id = id
        self.port = port
        self.config = config
        self.msgs = []
        self.conn_amount = 0

        threading.Thread(target=self.setup_connection).start()

    def setup_connection(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(self.config.cert_path)

        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn = ctx.wrap_socket(sock, server_hostname=self.config.hospital_ip)

                conn.bind((self.config.hospital_ip, self.config.num_port + self.id))
                conn.connect((self.config.hospital_ip, self.port))

                self.conn = conn
                self.conn_amount += 1

                print(f"connected to peer {self.id} ({self.port})")
                return

            except socket.error:
                print(f"could not connect to peer {self.id} ({self.port}), retrying in 5s...")
                sleep(5)

    def send_msg(self, msg):
        self.conn.sendall(msg.encode("utf-8"))

    def get_msg(self):
        while not self.msgs:
            sleep(1)
        return self.msgs.pop()

    def rcv_msg(self, conn, addr):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(Config.cert_path, Config.p_key_path)
        sock = context.wrap_socket(conn, server_side=True)
        self.conn_amount += 1

        while True:
            msg = sock.recv(1024)

            if len(msg) == 0:
                print(f"server at peer {self.id} : {self.port} stopped! Terminating process.")
                break

            self.msgs.append(msg)

        sock.close()
        self.conn.close()
        self.conn_amount = 0
