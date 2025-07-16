import socket
import threading

HOST = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024


def receive_messages(sock):
    while True:
        msg = sock.recv(BUFFER_SIZE).decode()
        print(msg)


def start_tcp_client():
    username = input("Kullanıcı adınızı girin: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, TCP_PORT))
    sock.send(username.encode())
    response = sock.recv(BUFFER_SIZE).decode()
    print(response)

    if "başka bir kullanıcı adı girin" in response:
        sock.close()
        return

    threading.Thread(target=receive_messages, args=(sock,)).start()

    while True:
        msg = input()
        if msg.lower() == "görüşürüz":
            sock.close()
            break
        sock.send(msg.encode())


if __name__ == "__main__":
    start_tcp_client()
