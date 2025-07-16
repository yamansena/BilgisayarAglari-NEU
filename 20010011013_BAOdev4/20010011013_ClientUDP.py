#20010011013-Sena YAMAN-ODEV-5

import socket
import threading

HOST = '127.0.0.1'
UDP_PORT = 12346
BUFFER_SIZE = 1024


def receive_messages(sock):
    while True:
        msg, _ = sock.recvfrom(BUFFER_SIZE)
        print(msg.decode())


def start_udp_client():
    username = input("Kullanıcı adınızı girin: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(username.encode(), (HOST, UDP_PORT))

    response, _ = sock.recvfrom(BUFFER_SIZE)
    print(response.decode())

    if "başka bir kullanıcı adı girin" in response.decode():
        sock.close()
        return

    threading.Thread(target=receive_messages, args=(sock,)).start()

    while True:
        msg = input()
        sock.sendto(f"{username}:{msg}".encode(), (HOST, UDP_PORT))
        if msg.lower() == "görüşürüz":
            break


if __name__ == "__main__":
    start_udp_client()
