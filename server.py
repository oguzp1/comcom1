"""
    Authors:
        Oguz Paksoy         - 150150111
        Merve Elif Demirtas - 150160706
    Date:
        18.3.2019
"""

from socket import *
import threading
import json
import os

questions = [
    {
        'id': 1,
        'question': 'Which one of the following can be classified as an access network?',
        'options': [
            'A Web server',
            'A personal computer which runs an application that connects to the Web',
            'Residential Wi-Fi',
            'End-point router of an international ISP connecting to a regional ISP'
        ]
    },
    {
        'id': 2,
        'question': 'Which one is true for both Peer-to-Peer and Server-Client architectures?',
        'options': [
            'A host with a static IP that transfers data is necessary for all clients',
            'Clients may come and go, and can also change IPs',
            'There always exists a mediator between two client end systems',
            'Multiple clients can directly connect to each other'
        ]
    },
    {
        'id': 3,
        'question': 'Which one of the following is an electronic mail protocol?',
        'options': [
            'SMTP',
            'HTTP',
            'FTP',
            'RFC'
        ]
    },
    {
        'id': 4,
        'question': 'What is the main difference between UDP and TCP?',
        'options': [
            'TCP is a faster and more reliable version of UDP',
            'TCP is connection oriented, UDP is connectionless',
            'UDP is a faster and more reliable version of TCP',
            'UDP is connection oriented, TCP is connectionless'
        ]
    },
    {
        'id': 5,
        'question': 'Which one of the following fields is not present on both TCP and UDP datagrams?',
        'options': [
            "Sender's Port Number",
            "Receiver's Port Number",
            'Checksum',
            'Acknowledgement Number'
        ]
    }
]

answers = [2, 1, 0, 1, 3]


class ThreadedServer:
    def listenToClient(self, client, addr):
        try:
            client.sendall('Please enter a username.'.encode())
            user = client.recv(1024).decode()

            userScores = [score for score in self.scores if score.startswith(user)]
            prevScores = ''.join(['{}) {}'.format(i + 1, result.split(': ', 1)[1])
                                  for i, result in zip(range(5), userScores)])

            client.sendall('Hello, {}! Your previous results are as follows:\n\n{}'.format(user, prevScores).encode())
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

                answersString = ', '.join(['({}: {:2d})'.format(i + 1, ans) for i, ans in enumerate(userAnswers)])
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
