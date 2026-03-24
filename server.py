import socket
import sys
import threading

clients = {}
clients_lock = threading.Lock()

def broadcast(message, sender=None):
    with clients_lock:
        for client in clients:
            if sender is not None and client is sender:
                continue
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(e)


def handle_client(connection, address):
    name = f'{address[0]}:{address[1]}'

    try:
        msg = connection.recv(1024).decode()
        if msg.startswith('Name:'):
            name = msg[5:].strip()
        with clients_lock:
            clients[connection] = name
        broadcast('Received from server: You can send message\n')
        print(f'{name} connect from {address}')
        broadcast(f'{name} join the conversation\n')
        while True:
            data = connection.recv(1024).decode()
            print(f'{name}: {data}')
            response = f'{name}: {data}'
            print('Sending data back to the client: ', response)
            broadcast(response, connection)
            if(data.lower() == 'quit'):
                break
    finally:
        connection.close()
        with clients_lock:
            clients.pop(connection, None)
        print(f'Close {name}')

def main():
    print('Starting Server')
    print('Create the socket')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print('Bind the socket to the port')
    server_address = ('127.0.0.1', 8084)

    print('Starting up on', server_address)
    sock.bind(server_address)

    print('Listen for incoming connections')
    sock.listen(10)
    print('Waiting for a connections')
    try:
        while True:
            connection, client_address = sock.accept()
            thread = threading.Thread(target=handle_client, args=(connection, client_address, ), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print('\nServer close')

if __name__ == '__main__':
    main()