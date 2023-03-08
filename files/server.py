"""
Stupid Server.py thing to prove i'm better than Agam Solomon.
"""
import threading
import socket
import json
import uuid

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8083))
server.listen(5)

CLIENTS = []
REMOTES = []

def handle_client(connection, address, password):
    thing = {
        'id': ID,
        'ip': address[0],
        'connection': connection,
        'password': password
    }
    CLIENTS.append(thing)
    connected = True
    while connected:
        message_length = connection.recv(64).decode('utf-8')
        if message_length:
            message = connection.recv(int(message_length)).decode('utf-8')
            message = json.loads(message)
            data = json.dumps(message).encode('utf-8')
            data_length = str(len(data)).encode('utf-8')
            data_length += b' ' * (64 - len(data_length))
            connection.send(data_length)
            connection.send(data)

def handle_remote(connection, address):
    REMOTES.append(connection)
    connected = True
    while connected:
        message_length = connection.recv(64).decode('utf-8')
        message = connection.recv(int(message_length)).decode('utf-8')
        message = json.loads(message)
        data = json.dumps(message).encode('utf-8')
        data_length = str(len(data)).encode('utf-8')
        data_length += b' ' * (64 - len(data_length))
        connection.send(data_length)
        connection.send(data)

def group_connection(c, a):
    message_length = c.recv(64).decode('utf-8')
    message = c.recv(int(message_length)).decode('utf-8')
    message = json.loads(message)
    f = handle_client if message['type'] == 'client' else handle_remote
    f(c, a, message['password'])
        

CONNECTIONS = []
LISTENING = True
ID = 0


while LISTENING:
    conn, addr = server.accept()
    ID += 1
    print('Connected by ', addr[0])
    threading.Thread(target=group_connection, args=(conn, addr)).start()
    CONNECTIONS.append(conn)
