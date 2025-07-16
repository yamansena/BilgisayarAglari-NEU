import threading
import socket

host = '127.0.0.1'  # localhost
TCP_PORT = 12345  # Match this with the new port number in server script
BUFFER_SIZE = 1024

username = input('Kullanıcı adı giriniz: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((host, TCP_PORT))
    client.send(b'user?')
    client.send(username.encode('utf-8'))
except Exception as e:
    print(f'Bağlantı kurulurken hata oluştu: {e}')
    client.close()
    exit()

def client_receive():
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode('utf-8')
            if not message:
                print('Bağlantı kesildi!')
                client.close()
                break
            print(message)
        except Exception as e:
            print(f'Alma işlemi sırasında hata oluştu: {e}')
            client.close()
            break

def client_send():
    while True:
        try:
            message = input("Mesajınızı girin: ")
            formatted_message = f'{message}'
            client.send(formatted_message.encode('utf-8'))
        except Exception as e:
            print(f'Mesaj gönderirken hata oluştu: {e}')
            client.close()
            break

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
