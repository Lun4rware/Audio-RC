import threading
import socket
import json
import random

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8083))
password = ''.join(random.choices('0123456789', k=8))

def send(message):
    data = {
        'message': ' '.join(message)
    }
    data = json.dumps(data).encode('utf-8')
    data_len = str(len(data)).encode('utf-8')
    data_len += b' ' * (64 - len(data_len))
    client.send(data_len)
    client.send(data)
    recieved_data_length = client.recv(64).decode('utf-8')
    recieved_data = client.recv(int(recieved_data_length))

the_data = {
    'type': 'client',
    'password': password
}

the_data = json.dumps(the_data).encode('utf-8')
the_data_len = str(len(the_data)).encode('utf-8')
the_data_len += b' ' * (64 - len(the_data_len))
client.send(the_data_len)
client.send(the_data)

def test(args):
    print(f'Test Command Args: {" ".join(arg for arg in args)}')


while True:
    commands = {
        "test": test,
        "send": send,
    }
    data = input('>> ').split(' ')
    command = commands.get(data[0].lower())
    args = data[1:]
    if command:
        command(args)
        continue
    print('Invalid Command!')
    # send(data)
