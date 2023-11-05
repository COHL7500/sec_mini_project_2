import ssl
import socket
import sys

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('./server.crt')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(sock, server_hostname="localhost")
conn.bind(("localhost", int(sys.argv[1])))
connected = False

print("port: ", sys.argv[1])

while not connected:
    try:
        conn.connect(("localhost", 6000))
        connected = True
    except socket.error:
        continue

while True:
    conn.sendall(input(": ").encode('UTF-8'))
