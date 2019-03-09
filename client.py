# CLIENT CODE

import socket



def client():
    host = socket.gethostname()
    port = 12000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client()