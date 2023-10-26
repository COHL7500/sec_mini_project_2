# patient.py
import socket
import ssl

# Hospital's IP and port
HOSPITAL_NAME = "localhost"
HOSPITAL_PORT = 12345
CERT_PATH = "server.crt"

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERT_PATH)

    patient_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    patient_socket.connect((HOSPITAL_NAME, HOSPITAL_PORT))

    patient_socket = context.wrap_socket(patient_socket, server_hostname=HOSPITAL_NAME)

    while True:
        request = input("Enter your medical request: ")
        patient_socket.send(request.encode('utf-8'))


if __name__ == "__main__":
    main()
