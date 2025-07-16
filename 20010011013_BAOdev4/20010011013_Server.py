# #20010011013-Sena YAMAN-ODEV-5
#
# #Kütüphaneler:
import socket
import threading

TCP_PORT = 12345
UDP_PORT = 12346
BUFFER_SIZE = 1024

tumclient = {}
clientLock = threading.Lock()


def handle_tcp_client(client_s, client_a):
    welcome_msg = "Chat'e hoşgeldin! Lütfen kullanıcı adınızı giriniz: "
    client_s.sendall(welcome_msg.encode())
    username = client_s.recv(BUFFER_SIZE).decode().strip()

    with clientLock:
        if username in [client['username'] for client in tumclient.values()]:
            client_s.sendall("Bu kullanıcı adı zaten alınmış, lütfen başka bir kullanıcı adı girin.".encode())
            client_s.close()
            return
        tumclient[client_a] = {'socket': client_s, 'username': username, 'protocol': 'TCP'}

    welcome_message = f"Hoşgeldiniz {username}! TCP bağlantınız için teşekkürler!"
    client_s.sendall(welcome_message.encode())
    broadcast(f"{username} [TCP] ile bağlanmıştır hoşgeldiniz")

    while True:
        try:
            message = client_s.recv(BUFFER_SIZE).decode()
            if not message:
                break
            print(f'{username}[TCP]: {message}')
            broadcast(f'{username}[TCP]: {message}', exclude=client_a)
        except ConnectionResetError:
            break

    with clientLock:
        del tumclient[client_a]
    client_s.close()
    broadcast(f"{username} sohbet odasından ayrıldı")


def tcp_ac(tcp_ss):
    while True:
        client_s, client_a = tcp_ss.accept()
        print(f'TCP bağlantısı {client_a}')
        threading.Thread(target=handle_tcp_client, args=(client_s, client_a)).start()


def udp_receive_m(udp_ss):
    while True:
        msg, client_a = udp_ss.recvfrom(BUFFER_SIZE)
        msg = msg.decode()

        with clientLock:
            if client_a in tumclient:
                if msg.strip().lower() == "görüşürüz":
                    username = tumclient[client_a]['username']
                    del tumclient[client_a]
                    print(f'{username} UDP Bağlantısı chatten ayrıldı.')
                    broadcast(f'{username} sohbet odasından ayrıldı')
                else:
                    username = tumclient[client_a]["username"]
                    messageprint = f"{username}[UDP]: {msg}"
                    print(messageprint)
                    broadcast(messageprint, exclude=client_a)
            else:
                if msg in [client['username'] for client in tumclient.values()]:
                    udp_ss.sendto("Bu kullanıcı adı zaten alınmış, lütfen başka bir kullanıcı adı girin".encode(),
                                  client_a)
                else:
                    tumclient[client_a] = {'username': msg, 'protocol': 'UDP'}
                    print(f'{msg} [UDP] ile bağlanmıştır hoşgeldiniz')
                    udp_ss.sendto(f"Hoşgeldiniz {msg}! UDP ile bağlısınız".encode(), client_a)


def broadcast(message, exclude=None):
    with clientLock:
        for address, client_info in tumclient.items():
            if address != exclude:
                if client_info['protocol'] == 'TCP':
                    try:
                        client_info['socket'].sendall(message.encode())
                    except Exception as e:
                        print(f'Error sending message to {address}: {e}')
                elif client_info['protocol'] == 'UDP':
                    try:
                        udp_ss.sendto(message.encode(), address)
                    except Exception as e:
                        print(f'Error sending message to {address}: {e}')


def start_server(tcp_port=TCP_PORT, udp_port=UDP_PORT):
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('localhost', tcp_port))
    tcp_server_socket.listen(5)
    print(f'TCP server listening on port {tcp_port}')

    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind(('localhost', udp_port))
    print(f'UDP server listening on port {udp_port}')

    global udp_ss
    udp_ss = udp_server_socket

    threading.Thread(target=tcp_ac, args=(tcp_server_socket,)).start()
    threading.Thread(target=udp_receive_m, args=(udp_server_socket,)).start()


if __name__ == '__main__':
    start_server()
