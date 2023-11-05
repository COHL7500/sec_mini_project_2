import ssl
import socket
import threading


def new_client(socket, addr):
    print(f'client connected, conn: {socket}, addr: {addr}')
    while True:
        msg = socket.recv(1024)
        print(addr, ": ", msg)

        if len(msg) == 0:
            print(f"client {addr} disconnected!")
            break
    socket.close()


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./server.crt', './priv.key')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 6000))
sock.listen(5)

print("server running...")

while True:
    conn, addr = sock.accept()
    ssock = context.wrap_socket(conn, server_side=True)
    threading.Thread(target=new_client, args=(ssock, addr)).start()
