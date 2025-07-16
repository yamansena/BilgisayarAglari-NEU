import threading
import socket

UDP_HOST = '127.0.0.1'  # localhost
UDP_PORT = 12346  # Match this with the new port number in server script
BUFFER_SIZE = 1024

username = input('Kullanıcı adı giriniz: ')

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'user?', (UDP_HOST, UDP_PORT))
client.sendto(username.encode('utf-8'), (UDP_HOST, UDP_PORT))

def client_receive():
    while True:
        try:
            data, addr = client.recvfrom(BUFFER_SIZE)
            print(data.decode('utf-8'))
        except ConnectionResetError:
            print('Connection was closed by the server.')
            break
        except Exception as e:
            print(f'Error: {e}')
            client.close()
            break

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

try:
    while True:
        message = input("Mesajınızı girin: ")
        formatted_message = f'{username}: {message}'  # Corrected the formatting here
        client.sendto(formatted_message.encode('utf-8'), (UDP_HOST, UDP_PORT))
except KeyboardInterrupt:
    print("Program stopped by the user.")
    client.close()
