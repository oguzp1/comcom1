# SERVER CODE

# TCP socket, threaded server, example 2
# this server receives a message from client and print it on screen, then wait for another connection requests as well as listen for connected clients

from socket import *
import threading
import json
import os

questions = [
    {
        'id': 1,
        'question': 'Soru 1',
        'options': [
            'A1',
            'B1',
            'C1',
            'D1'
        ]
    },
    {
        'id': 2,
        'question': 'Soru 2',
        'options': [
            'A2',
            'B2',
            'C2',
            'D2'
        ]
    },
    {
        'id': 3,
        'question': 'Soru 3',
        'options': [
            'A3',
            'B3',
            'C3',
            'D3'
        ]
    },
    {
        'id': 4,
        'question': 'Soru 4',
        'options': [
            'A4',
            'B4',
            'C4',
            'D4'
        ]
    },
    {
        'id': 5,
        'question': 'Soru 5',
        'options': [
            'A5',
            'B5',
            'C5',
            'D5'
        ]
    }
]

answers = [0, 0, 0, 0, 0]

class ThreadedServer:
    def listenToClient(self, client, addr):
        try:
            client.sendall('Please enter a username.'.encode())
            user = client.recv(1024).decode()

            userScores = [score for score in self.scores if score.startswith(user)]
            prevScores = ''.join(['{}) {}'.format(i + 1, result.split(': ', 1)[1])
                                    for i, result in zip(range(5), userScores)])

            client.sendall('Hello, {}! Your previous results are as follows:\n{}'.format(user, prevScores).encode())
            mode = client.recv(1024).decode()

            if mode == 'exit':
                client.close()
            elif mode == 'begin':
                score = 0
                userAnswers = []

                client.sendall(str(len(questions)).encode())

                if int(client.recv(1024).decode()) != len(questions):
                    client.close()
                    exit(1)

                for i in range(len(questions)):
                    client.sendall(json.dumps(questions[i]).encode())
                    answer = int(client.recv(1024).decode())
                    userAnswers.append(answer)

                    if answer == answers[i]:
                        score += 1
                        client.sendall('Correct answer.'.encode())
                    else:
                        client.sendall('Incorrect answer.'.encode())

                client.sendall('Quiz complete. You scored {} / {}'.format(score, len(questions)).encode())
                client.close()

                answersString = ', '.join(['({}: {})'.format(i + 1, ans) for i, ans in enumerate(userAnswers)])
                self.scores.insert(0, '{}: {} / {} [Answers: {}]\n'.format(user, score, len(questions), answersString))
            else:
                client.close()
                exit(1)
        except:
            print('Connection to {} was aborted before the quiz ended.'.format(addr))
            exit(1)

        exit(0)

    def __init__(self, scores):
        self.scores = scores

    def startOnPort(self, serverPort):
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
        except:
            print("Socket cannot be created!!!")
            exit(1)

        print("Socket is created...")

        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print("Socket cannot be used!!!")
            exit(1)

        print("Socket is being used...")

        try:
            serverSocket.bind(('', serverPort))
        except:
            print("Binding cannot de done!!!")
            exit(1)

        print("Binding is done...")

        try:
            serverSocket.listen(45)
        except:
            print("Server cannot listen!!!")
            exit(1)

        print("The server is ready to receive")

        while True:
            connectionSocket = None
            try:
                serverSocket.settimeout(10)
                connectionSocket, addr = serverSocket.accept()
                threading.Thread(target=self.listenToClient, args=(connectionSocket, addr), daemon=True).start()
            except timeout:
                continue
            except KeyboardInterrupt:
                if connectionSocket:
                    connectionSocket.close()
                serverSocket.close()
                break

    def getScores(self):
        return self.scores


if __name__ == '__main__':
    serverPort = 12000

    if os.path.exists('results.txt'):
        with open('results.txt', 'r') as readResultsFile:
            results = readResultsFile.readlines()
    else:
        results = []

    server = ThreadedServer(results)
    try:
        server.startOnPort(serverPort)
    except KeyboardInterrupt:
        scores = server.getScores()
        with open('results.txt', 'w') as writeResultsFile:
            writeResultsFile.writelines(scores)
