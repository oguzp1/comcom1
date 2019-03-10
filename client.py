"""
    Authors:
        Oguz Paksoy         - 150150111
        Merve Elif Demirtas - 150160706
    Date:
        10.3.2019
"""

import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGroupBox, QGridLayout, QLineEdit, \
    QPushButton, QRadioButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
import json


class App(QMainWindow):
    def __init__(self, clientSocket):
        super(App, self).__init__()
        self.title = 'Quiz Application'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 400
        self.clientSocket = clientSocket
        self.remainingQuestions = -1

        self.initUI()

    def tcpReceiveString(self):
        try:
            return self.clientSocket.recv(1024).decode()
        except:
            self.clientSocket.close()
            self.close()
            raise

    def tcpSendString(self, string):
        try:
            self.clientSocket.sendall(string.encode())
        except:
            self.clientSocket.close()
            self.close()
            raise

    def startPageSetup(self):
        self.labelPrimary = QLabel()
        self.labelPrimary.setAlignment(Qt.AlignCenter)
        self.labelPrimary.setFixedWidth(500)

        self.lineEdit = QLineEdit('')
        self.lineEdit.setFixedWidth(500)
        self.lineEdit.setFixedHeight(30)

        self.buttonPrimary = QPushButton('Enter')
        self.buttonPrimary.clicked.connect(self.enter)

        self.layout.addWidget(self.labelPrimary, 0, 1, Qt.AlignBottom)
        self.layout.addWidget(self.lineEdit, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.buttonPrimary, 2, 1, Qt.AlignTop)

        self.labelPrimary.setText(self.tcpReceiveString())

    def welcomePageSetup(self):
        self.layout.removeWidget(self.lineEdit)
        self.lineEdit.deleteLater()

        self.layout.removeWidget(self.buttonPrimary)
        self.buttonPrimary.disconnect()

        self.buttonPrimary.setText("Let's Start!")
        self.buttonPrimary.setFixedHeight(30)
        self.buttonPrimary.setFixedWidth(500)
        self.buttonPrimary.clicked.connect(self.startQuiz)

        self.buttonSecondary = QPushButton('Exit')
        self.buttonSecondary.setFixedHeight(30)
        self.buttonSecondary.setFixedWidth(500)
        self.buttonSecondary.clicked.connect(self.exitBeforeQuiz)

        self.layout.addWidget(self.buttonPrimary, 2, 1, Qt.AlignBottom)
        self.layout.addWidget(self.buttonSecondary, 3, 1, Qt.AlignTop)

    def quizPageSetup(self):
        self.layout.removeWidget(self.buttonPrimary)
        self.buttonPrimary.disconnect()

        self.layout.removeWidget(self.buttonSecondary)
        self.buttonSecondary.deleteLater()

        self.layout.removeWidget(self.labelPrimary)

        self.vBox = QWidget()
        vBoxLayout = QVBoxLayout()

        self.radios = [QRadioButton('answer') for _ in range(4)]

        for i in range(4):
            vBoxLayout.addWidget(self.radios[i], Qt.AlignCenter)

        self.vBox.setLayout(vBoxLayout)

        self.buttonPrimary.setText('Check')
        self.buttonPrimary.setFixedWidth(300)
        self.buttonPrimary.clicked.connect(self.checkQuestion)

        self.labelResult = QLabel('Result: ')

        self.layout.addWidget(self.labelPrimary, 0, 1, Qt.AlignCenter)
        self.layout.addWidget(self.vBox, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.buttonPrimary, 2, 1, Qt.AlignCenter)
        self.layout.addWidget(self.labelResult, 3, 1, Qt.AlignCenter)

    def resultPageSetup(self):
        self.layout.removeWidget(self.vBox)
        self.vBox.deleteLater()

        self.buttonPrimary.disconnect()

        self.layout.removeWidget(self.labelResult)
        self.labelResult.deleteLater()

        self.buttonPrimary.setText('Exit')
        self.buttonPrimary.setFixedWidth(300)
        self.buttonPrimary.clicked.connect(self.exit)

    def enter(self):
        # send username
        self.tcpSendString(self.lineEdit.text())

        # recv prev scores
        self.labelPrimary.setText(self.tcpReceiveString())

        self.welcomePageSetup()

    def startQuiz(self):
        # send begin code
        self.tcpSendString('begin')

        # receive question count
        self.remainingQuestions = int(self.tcpReceiveString())

        # send acknowledgement
        self.tcpSendString(str(self.remainingQuestions))

        self.quizPageSetup()

        self.askQuestion()

    def askQuestion(self):
        if self.remainingQuestions > 0:
            question = json.loads(self.tcpReceiveString())

            self.labelPrimary.setText('Question {}:\n{}'.format(question['id'], question['question']))
            for i in range(4):
                self.radios[i].setText(question['options'][i])

            self.labelResult.setText('Result: ')
            self.buttonPrimary.setText('Check')
            self.buttonPrimary.disconnect()
            self.buttonPrimary.clicked.connect(self.checkQuestion)
            self.remainingQuestions -= 1
        else:
            self.showResults()

    def checkQuestion(self):
        ans = next((i for i in range(4) if self.radios[i].isChecked()), -1)

        # send answer
        self.tcpSendString(str(ans))

        self.buttonPrimary.setText('Next')
        self.buttonPrimary.disconnect()
        self.buttonPrimary.clicked.connect(self.askQuestion)

        # receive answer status
        self.labelResult.setText('Result: ' + self.tcpReceiveString())

    def showResults(self):
        # receive final score
        self.labelPrimary.setText(self.tcpReceiveString())

        self.resultPageSetup()

    def exit(self):
        self.clientSocket.close()
        self.close()

    def exitBeforeQuiz(self):
        self.tcpSendString('exit')
        self.exit()

    def initUI(self):
        # Write GUI initialization code

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        self.horizontalGroupBox = QGroupBox('Quiz Application')
        self.layout = QGridLayout()
        self.horizontalGroupBox.setLayout(self.layout)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        wid.setLayout(windowLayout)

        self.startPageSetup()

        self.show()


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 12000

    clientSocket = socket.socket()
    try:
        clientSocket.connect((host, port))
    except:
        clientSocket.close()
        exit(1)

    app = QApplication(sys.argv)
    ex = App(clientSocket)
    sys.exit(app.exec_())
