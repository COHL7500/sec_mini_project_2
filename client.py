import socket
import ssl
import threading

HOSPITAL_NAME = "localhost"
HOSPITAL_PORT = 12345
CERT_PATH = "server.crt"
P_KEY_PATH = "priv.key"
ids = [0, 1, 2, 3]


def rcv_msg(ssl_socket: ssl.SSLSocket):
    while True:
        msg = ssl_socket.recv(1024).decode('utf-8')
        if not msg:
            break
        print(f"msg received: {msg}")


def send_msg(peer_id, msg):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERT_PATH)

    if peer_id in ids:
        ssl_socket = context.wrap_socket(socket.create_connection(("127.0.0.1", (peer_id + 12345))), server_hostname="localhost")
        ssl_socket.send(msg.encode('utf-8'))
        ssl_socket.close()
    else:
        print(f"Peer '{peer_id}' not found")


def find_port():
    for port in range(HOSPITAL_PORT, HOSPITAL_PORT + 5):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.bind(("127.0.0.1", port))
            peer_socket.close()
            peer_id = port - 12345
            ids.remove(peer_id)
            print(ids)
            return port, peer_id
        except OSError:
            continue
    raise Exception("Max number of users has been found.")


def handle_patient(patient_socket, addr):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT_PATH, P_KEY_PATH)
    context.load_verify_locations(CERT_PATH)

    patient_socket = context.wrap_socket(patient_socket, server_side=True, do_handshake_on_connect=True)

    rcv_msg(patient_socket)
    patient_socket.close()
    print("Connection with {}:{} closed.".format(addr[0], addr[1]))


def main():
    peer_port, peer_id = find_port()

    # Patients
    if peer_id != 0:
        print(f"Peer listening on port {peer_port}")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", peer_port))
        server_socket.listen(5)

        while True:
            recipient, msg = input("Recipient name and message '1 Hi': ").split()

            if msg.lower() == "quit":
                break

            if recipient == peer_id:
                print("You cannot send a message to yourself")
                continue

            send_msg(int(recipient), msg)

    # Hospital
    else:
        print("You're the hospital!")
        print("Hospital is listening: {}:{}".format(HOSPITAL_NAME, HOSPITAL_PORT))

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOSPITAL_NAME, HOSPITAL_PORT))
        server_socket.listen(5)

        while True:
            client_socket, addr = server_socket.accept()

            print("Accepted connection from {}:{}".format(addr[0], addr[1]))

            patient_thread = threading.Thread(target=handle_patient, args=(client_socket, addr))
            patient_thread.start()


if __name__ == "__main__":
    main()
