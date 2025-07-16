import socket
BUFFER_SIZE = 1024
def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        username = input("Kullanıcı adı: ")
        full_message = f"{username}:"
        client_socket.sendto(full_message.encode('utf-8'), ("127.0.0.1", 12346))
        response, _ = client_socket.recvfrom(BUFFER_SIZE)
        print(response.decode('utf-8'))
        if "Hoşgeldiniz" in response.decode('utf-8'):
            break

    while True:
        message = input("Mesaj: ")
        if message == 'görüşürüz' or message == 'GÖRÜŞÜRÜZ':
            full_message = f"{username}:görüşürüz"
            client_socket.sendto(full_message.encode('utf-8'), ("127.0.0.1", 12346))
            break
        full_message = f"{username}:{message}"
        client_socket.sendto(full_message.encode('utf-8'), ("127.0.0.1", 12346))

    client_socket.close()

if __name__ == "__main__":
    udp_client()
