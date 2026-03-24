import socket
import threading
import random
import streamlit as st

if "sock" not in st.session_state:
    st.session_state.sock = None
if "connection" not in st.session_state:
    st.session_state.connect = None
if "thread" not in st.session_state:
    st.session_state.thread = None
if "name" not in st.session_state:
    st.session_state.name = ''
if "messages" not in st.session_state:
    st.session_state.messages = []


def received_message(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            st.session_state.messages.append(data)
            print(f'\n{data}')
        except OSError:
            break

def connect():
    if st.session_state.sock is None:
        num = random.randrange(1, 1000)
        print('Starting Client')
        print('Create a TCP/IP socket')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        st.session_state.sock = sock

        print('Connect the socket to server port')
        server_address = ('127.0.0.1', 8084)
        print('Connecting to: ', server_address)
        connection = sock.connect(server_address)
        st.session_state.connection = connection
        print('Connected to server')
        st.session_state.sock.send(f'Name:Client {num}'.encode())
        st.session_state.name = f'Client {num}'

        thread = threading.Thread(target=received_message, args=(sock, ), daemon=True)
        thread.start()
        st.session_state.thread = thread

def disconnect():
    st.session_state.messages.append('Close socket')
    print('Close socket')
    st.session_state.sock.close()
    st.session_state.sock = None
    st.session_state.connection = None

def main():
    connect()
    
    st.text('Send data')
    message = st.chat_input()
    if message:
        st.session_state.messages.append(f'Sending: {message}')
        st.session_state.messages.append(f'{st.session_state.name}: {message}')
        print(f'{st.session_state.name}: {message}')
        st.session_state.sock.send(str(message).encode())

        if message.lower() == 'quit':
            disconnect()

    for msg in st.session_state.messages:
        st.write(msg)
        st.divider()


if __name__ == '__main__':
    main()