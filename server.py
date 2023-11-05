import socket
from threading import Thread
from time import sleep

import PeerFactory
from config import Config
from patient import Patient


class Server(Thread):
    def __init__(self, config, peer_factory: PeerFactory.PeerFactory):
        super(Server, self).__init__()
        self.config = config
        self.peers = []
        self.peer_factory = peer_factory

        self.setup_server_socket()

    def setup_server_socket(self):
        try:
            print(f"server port: {Config.num_port}")

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.config.hospital_ip, self.config.num_port))
            self.server_socket.listen(self.config.peer_amount)
            print("server running...")

        except socket.error:
            print("failed socket error")
            exit()

        self.setup_peers()

    def run(self):
        while True:
            client_socket, address = self.server_socket.accept()
            peer = self.find_peer(int(address[1]))

            thread = Thread(target=peer.rcv_msg, args=(client_socket, address))
            thread.start()

            print(f"peer {address[1]} connected to local server")

    def setup_peers(self):
        for client_port in (range(
                self.config.hospital_port,
                self.config.hospital_port + self.config.max_port * self.config.peer_amount + 1,
                self.config.max_port)
        ):

            if client_port != Config.num_port:
                self.peers.append(self.peer_factory.create_peer(self.config, client_port, len(self.peers) + 1))
               # self.peers.append(Patient(self.config, client_port, len(self.peers) + 1))

    def wait_for_peers(self):
        while True:
            for p in self.peers:
                if p.conn_amount != 2:
                    sleep(2)
                    break
            else:
                print("peers are now all connected...")
                return

    def find_peer(self, port: int):
        return next(i for i in self.peers if ((port % i.port) <= Config.peer_amount))

    def send_msg_peer(self, peer: int, msg):
        self.peers[peer].send_msg(msg)

    def get_msg_peer(self, peer: int):
        return self.peers[peer].get_msg()
