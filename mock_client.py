# CLIENT CODE

import socket
import json


def client():
    host = '127.0.0.1'
    port = 12000
    client_socket = socket.socket()
    client_socket.connect((host, port))

    # receive username question
    user_question = client_socket.recv(1024).decode()
    user = input(user_question)
    client_socket.sendall(user.encode())

    # receive prev scores
    prev_scores = client_socket.recv(1024).decode()
    print(prev_scores)
    mode = input('Enter mode (exit, begin): ')
    client_socket.sendall(mode.encode())
    if mode != 'begin':
        client_socket.close()
        return

    # receive question count
    question_count = int(client_socket.recv(1024).decode())

    for i in range(question_count):
        # receive question
        question = json.loads(client_socket.recv(1024).decode())
        print(question['question'])
        for j, opt in enumerate(question['options']):
            print(j, opt)
        answer = input('Your answer: ')

        client_socket.sendall(answer.encode())

        # receive message
        ans_message = client_socket.recv(1024).decode()
        print(ans_message)

    # receive final score
    score_str = client_socket.recv(1024).decode()
    print(score_str)
    client_socket.close()


if __name__ == '__main__':
    client()
