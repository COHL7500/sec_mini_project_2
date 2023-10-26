import socket
import ssl
import threading

HOSPITAL_NAME = "localhost"
HOSPITAL_PORT = 12345
CERT_PATH = "server.crt"
P_KEY_PATH = "priv.key"


def handle_patient(patient_socket, addr):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT_PATH, P_KEY_PATH)
    context.load_verify_locations(CERT_PATH)

    patient_socket = context.wrap_socket(patient_socket, server_side=True, do_handshake_on_connect=True)

    while True:
        request = patient_socket.recv(1024).decode('utf-8')
        if not request:
            break

        print("Request received from {}: {}".format(addr[0], request))

    patient_socket.close()
    print("Connection with {}:{} closed.".format(addr[0], addr[1]))


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOSPITAL_NAME, HOSPITAL_PORT))
    server_socket.listen(5)

    print("Hospital is listening: {}:{}".format(HOSPITAL_NAME, HOSPITAL_PORT))

    while True:
        client_socket, addr = server_socket.accept()
        print("Accepted connection from {}:{}".format(addr[0], addr[1]))

        patient_thread = threading.Thread(target=handle_patient, args=(client_socket, addr))
        patient_thread.start()


if __name__ == "__main__":
    main()
