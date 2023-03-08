import threading
import socket
import json

remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remote.connect(('127.0.0.1', 8083))

def send(message):
    data = {
        'message': message
    }
    data = json.dumps(data).encode('utf-8')
    data_len = str(len(data)).encode('utf-8')
    data_len += b' ' * (64 - len(data_len))
    print(data_len, data)
    remote.send(data_len)
    remote.send(data)
    recieved_data_length = remote.recv(64).decode('utf-8')
    recieved_data = remote.recv(int(recieved_data_length))

the_data = {
    'type': 'remote'
}

the_data = json.dumps(the_data).encode('utf-8')
the_data_len = str(len(the_data)).encode('utf-8')
the_data_len += b' ' * (64 - len(the_data_len))
remote.send(the_data_len)
remote.send(the_data)

while True:
    data = input('>> ')
    send(data)
