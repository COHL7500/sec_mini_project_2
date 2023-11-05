import socket
from threading import Thread
from time import sleep
import PeerFactory
from config import Config


class Server(Thread):
    def __init__(self, config: Config, peer_factory: PeerFactory.PeerFactory):
        super(Server, self).__init__()
        self.server_socket = None
        self.config = config
        self.peer_list = []
        self.peer_factory = peer_factory

        self.setup_server_socket()

    def setup_server_socket(self):
        try:
            print(f"server port: {Config.num_port}")

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.config.hospital_ip, self.config.num_port))
            self.server_socket.listen(self.config.peer_amount)

        except socket.error:
            print("failed socket error")
            exit()

        print("server running...")
        self.setup_peers()

    def run(self):
        while True:
            client_socket, address = self.server_socket.accept()
            peer = self.find_peer(int(address[1]))

            thread = Thread(target=peer.receive_message, args=(client_socket, address))
            thread.start()

            print(f"peer {address[1]} connected to local server")

    def setup_peers(self):

        for client_port in (range(
                self.config.hospital_port,
                self.config.hospital_port + self.config.max_port * self.config.peer_amount + 1,
                self.config.max_port)
        ):
            peer_id = len(self.peer_list) + 1

            if client_port != Config.num_port:
                self.peer_list.append(self.peer_factory.create_peer(self.config, client_port, peer_id))

    def wait_for_peers(self):
        while True:
            for p in self.peer_list:
                if p.total_connected != 2:
                    sleep(2)
                    break
            else:
                print("Successfully connected all peers!")
                return

    def get_message_from_peer(self, peer: int):
        return self.peer_list[peer].get_message()

    def find_peer(self, port: int):
        return next(i for i in self.peer_list if ((port % i.port) <= Config.peer_amount))

    def send_message_to_peer(self, peer: int, msg):
        self.peer_list[peer].send_message(msg)
