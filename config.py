from sys import argv


class Config:
    hospital_ip = 'localhost'
    cert_path = './server.crt'
    p_key_path = './priv.key'
    peer_amount = 3
    max_port = peer_amount + 1
    peer_id = int(argv[1])
    hospital_port = 5000
    num_port = hospital_port + max_port * peer_id
