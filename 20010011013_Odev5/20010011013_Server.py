import threading
import socket

host = '127.0.0.1'  # localhost
TCP_PORT = 12345  # Port number for TCP
UDP_PORT = 12346  # Port number for UDP
BUFFER_SIZE = 1024

# TCP ve UDP için ayrı soketler oluştur
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind((host, TCP_PORT))
tcp_server.listen()

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_server.bind((host, UDP_PORT))

print('Sunucular başlatıldı...')

# Bu istemcileri bir veri yapısında tutmamız gerekiyor
tcp_clients = {}
udp_clients = {}

# Broadcast işlemi ile ağdaki tüm cihazlara dağıtımı sağlamamız gerekiyor
def broadcast_tcp(message):
    for client in list(tcp_clients.keys()):
        try:
            client.send(message)
        except:
            client.close()
            del tcp_clients[client]

def broadcast_udp(message):
    for addr in udp_clients.keys():
        udp_server.sendto(message, addr)

# TCP istemcileri işleme al
def handle_tcp_client(client, address):
    username = ""
    while True:
        try:
            if not username:
                client.send("Hoşgeldiniz! Lütfen kullanıcı adınızı girin: ".encode('utf-8'))
                username = client.recv(BUFFER_SIZE).decode('utf-8')
                if username in tcp_clients.values() or username in udp_clients.values():
                    client.send("Bu kullanıcı adı zaten alınmış, lütfen başka bir kullanıcı adı girin.".encode('utf-8'))
                    username = ""
                else:
                    tcp_clients[client] = username
                    broadcast_tcp(f"{username}[TCP] ile bağlandı. Hoşgeldiniz!".encode('utf-8'))
            else:
                message = client.recv(BUFFER_SIZE)
                formatted_message = f"{username}[TCP] : {message.decode('utf-8')}"
                broadcast_tcp(formatted_message.encode('utf-8'))
        except:
            if client in tcp_clients:
                username = tcp_clients[client]
                del tcp_clients[client]
                client.close()
                broadcast_tcp(f"{username} odadan ayrıldı!".encode('utf-8'))
            break

# TCP istemcileri kabul et
def accept_tcp_clients():
    while True:
        print('TCP Sunucusu çalışıyor ve dinleniyor...')
        client, address = tcp_server.accept()
        print(f'Bağlantı kuruldu {str(address)} ile')
        thread = threading.Thread(target=handle_tcp_client, args=(client, address))
        thread.start()

# UDP istemcileri işleme al
def handle_udp_clients():
    while True:
        print('UDP Sunucusu çalışıyor ve dinleniyor...')
        data, addr = udp_server.recvfrom(BUFFER_SIZE)
        if data == b'user?':
            username = udp_server.recvfrom(BUFFER_SIZE)[0].decode('utf-8')
            if username in tcp_clients.values() or username in udp_clients.values():
                udp_server.sendto("Bu kullanıcı adı zaten alınmış, lütfen başka bir kullanıcı adı girin.".encode('utf-8'), addr)
            else:
                udp_clients[addr] = username
                udp_server.sendto(f"Hoşgeldiniz {username}[UDP] ile bağlısınız".encode('utf-8'), addr)
                broadcast_tcp(f"{username}[UDP] ile bağlandı. Hoşgeldiniz!".encode('utf-8'))
        else:
            username = udp_clients.get(addr, "Unknown")
            formatted_message = f"{username}[UDP] : {data.decode('utf-8')}"
            broadcast_udp(formatted_message.encode('utf-8'))

if __name__ == "__main__":
    tcp_thread = threading.Thread(target=accept_tcp_clients)
    udp_thread = threading.Thread(target=handle_udp_clients)
    tcp_thread.start()
    udp_thread.start()
