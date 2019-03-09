# CLIENT CODE
import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QGridLayout, QLineEdit, qApp, QPushButton, QMessageBox, QButtonGroup, QRadioButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt



class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Quiz Application'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 400

        self.initUI()

    def start(self):
        self.layout.removeWidget(self.b2)
        self.b2.deleteLater()

        self.layout.removeWidget(self.b3)
        self.b3.deleteLater()

        self.layout.removeWidget(self.ql)
        self.ql.deleteLater()

        self.ql3 = QLabel("Question 1")

        self.layout.addWidget(self.ql3, 0, 1, Qt.AlignCenter)

        vBox = QWidget()
        vBox2 = QVBoxLayout()

        radio1 = QRadioButton("answer 1")
        radio2 = QRadioButton("answer 2")
        radio3 = QRadioButton("answer 3")
        radio4 = QRadioButton("answer 4")

        vBox2.addWidget(radio1)
        vBox2.addWidget(radio2)
        vBox2.addWidget(radio3)
        vBox2.addWidget(radio4)

        vBox.setLayout(vBox2)

        self.b4 = QPushButton("Check")
        self.b4.setFixedHeight(30)
        self.b4.setFixedWidth(300)
        self.b4.clicked.connect(self.check)

        hBox = QWidget()
        hBox2 = QHBoxLayout()

        self.ql4 = QLabel("Result: ")
        self.ql5 = QLabel("")

        hBox2.addWidget(self.ql4)
        hBox2.addWidget(self.ql5)

        hBox.setLayout(hBox2)

        self.layout.addWidget(vBox, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.b4, 2, 1, Qt.AlignCenter)
        self.layout.addWidget(hBox, 3, 1, Qt.AlignCenter)


    def check(self):
        self.b4.setText("Next")
        self.b4.clicked.connect(self.next)

        self.ql5.setText("True/False")


    def next(self):

        self.ql3.setText("Question 2...")
        self.b4.setText("Check")
        self.b4.clicked.connect(self.check)

        self.ql5.setText("")


    def exit(self):
        pass


    def enter(self):
        self.layout.removeWidget(self.ql2)
        self.ql2.deleteLater()

        self.layout.removeWidget(self.b1)
        self.b1.deleteLater()

        self.ql.setText("Welcome, your previous score is ...")

        self.b2 = QPushButton("Let's Start")
        self.b2.setFixedHeight(30)
        self.b2.setFixedWidth(300)
        self.b2.clicked.connect(self.start)

        self.b3 = QPushButton('Exit')
        self.b3.setFixedHeight(30)
        self.b3.setFixedWidth(300)
        self.b3.clicked.connect(self.exit)

        self.layout.addWidget(self.b2, 2, 1, Qt.AlignBottom)
        self.layout.addWidget(self.b3, 3, 1, Qt.AlignTop)



    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Quiz Application")

        self.layout = QGridLayout()

        self.ql = QLabel('Hello, please enter your username!')
        self.ql.setAlignment(Qt.AlignCenter)
        self.ql.setFixedHeight(20)
        self.ql.setFixedWidth(300)

        self.ql2 = QLineEdit('')
        self.ql2.setFixedWidth(300)
        self.ql2.setFixedHeight(30)

        self.b1 = QPushButton('Enter')
        self.b1.clicked.connect(self.enter)

        self.layout.addWidget(self.ql, 0, 1, Qt.AlignBottom)
        self.layout.addWidget(self.ql2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.b1, 2, 1, Qt.AlignTop)

        self.horizontalGroupBox.setLayout(self.layout)

    def initUI(self):
        # Write GUI initialization code

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        wid.setLayout(windowLayout)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


"""
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

"""