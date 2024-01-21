import socket
import threading
import datetime
import time

from protocol import Message, OperandText, SaveMessage, encrypt_string, decrypt_string
from constants import *

ALL_USER = {}
MESSAGES = []
USER_MESSAGE = {}


class Server:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((TCP_HOST, TCP_PORT))
        self.tcp_socket.listen(SERVER_MAX_CONNECTION)
        print('Running on: ' + f'{TCP_HOST}:{TCP_PORT}')

        threading.Thread(target=self.start_tcp_server, args=()).start()

    def start_tcp_server(self):
        while True:
            connection, _ = self.tcp_socket.accept()
            threading.Thread(target=self.authenticate, args=(connection,)).start()

    def authenticate(self, connection: socket):
        message = Message(datetime.datetime.now(), GET_USERNAME_TEXT, SERVER_USERNAME)
        self.send_message(connection, message)
        username = self.get_one_message(connection)
        user_data = ALL_USER.get(username)
        if user_data:
            if user_data['connection'] == UserCondition.online:
                message = Message(datetime.datetime.now(), ANOTHER_ACCOUNT_ALREADY_ONLINE, SERVER_USERNAME)
                self.send_message(connection, message)
                time.sleep(0.1)
                connection.shutdown(socket.SHUT_RDWR)
            else:
                message = Message(datetime.datetime.now(), GET_PASSWORD_TEXT, SERVER_USERNAME)
                self.send_message(connection, message)
                password = self.get_one_message(connection)
                if user_data['password'] == encrypt_string(password, ENCRYPT_KEY):
                    ALL_USER[username]['connection'] = connection
                    ALL_USER[username]['condition'] = UserCondition.online
                    ALL_USER[username]['mode'] = UserMode.available
                    message = Message(datetime.datetime.now(), WELCOME_MESSAGE, SERVER_USERNAME)
                    self.send_message(connection, message)
                    self.handle_client(username)
                else:
                    message = Message(datetime.datetime.now(), WRONG_PASSWORD, SERVER_USERNAME)
                    self.send_message(connection, message)
                    time.sleep(0.1)
                    connection.shutdown(socket.SHUT_RDWR)
        else:
            message = Message(datetime.datetime.now(), GET_NEW_PASSWORD_TEXT, SERVER_USERNAME)
            self.send_message(connection, message)
            password = self.get_one_message(connection)
            ALL_USER[username] = {'password': encrypt_string(password, ENCRYPT_KEY), 'connection': connection,
                                  'condition': UserCondition.online, 'mode': UserMode.available}
            message = Message(datetime.datetime.now(), WELCOME_MESSAGE, SERVER_USERNAME)
            self.send_message(connection, message)
            self.handle_client(username)

    def get_one_message(self, connection):
        while True:
            try:
                msg = connection.recv(MESSAGE_MAX_LENGTH)
            except:
                connection.shutdown(socket.SHUT_RDWR)
                break
            if msg:
                decoded_message = Message.decode_message(msg)
                return decoded_message.text

        return False

    def broadcast_message_to_users(self, users, message):
        for username in users:
            other_user_data = ALL_USER.get(username)
            if other_user_data and other_user_data['condition'] == UserCondition.online:
                if other_user_data['mode'] == UserMode.available:
                    self.send_message(other_user_data['connection'], message)

    def save_messages(self, fr, to_users, date, text):
        for user in to_users:
            mes = SaveMessage(fr, user, date, text)
            MESSAGES.append(mes)

    def user_messages(self, username):
        for mes in MESSAGES:
            if mes.fr == username or mes.to == username:
                self.send_message(ALL_USER[username]['connection'],
                                  Message(mes.date, mes.convert_to_string(), SERVER_USERNAME))

    def check_clients_status(self, connection, username):
        while True:
            time.sleep(1)
            try:
                connection.send('heartbeat'.encode())
            except:
                ALL_USER[username]['condition'] = UserCondition.offline
                print('connection lost. username: %s', username)
                connection.close()
                break

    def handle_client(self, username):
        user_data = ALL_USER[username]
        connection = user_data['connection']
        print('new connection. username: %s', username)
        threading.Thread(target=self.check_clients_status, args=(connection, username)).start()
        while True:
            try:
                msg = connection.recv(MESSAGE_MAX_LENGTH)
            except:
                break
            if msg:
                decoded_message = Message.decode_message(msg, username)
                o_t = OperandText.get_text(decoded_message.text)
                operand = o_t.operand
                if operand == 'Mode':
                    if o_t.to == "A":
                        ALL_USER[username]['mode'] = UserMode.available
                        message = Message(datetime.datetime.now(), CHANGE_MODE_TO_AVAILABLE, SERVER_USERNAME)
                        self.send_message(connection, message)
                    else:
                        ALL_USER[username]['mode'] = UserMode.busy
                        message = Message(datetime.datetime.now(), CHANGE_MODE_TO_BUSY, SERVER_USERNAME)
                        self.send_message(connection, message)

                if ALL_USER[username]['mode'] == UserMode.busy:
                    message = Message(datetime.datetime.now(), BUSY_MODE, SERVER_USERNAME)
                    self.send_message(connection, message)
                    continue

                if operand == 'P' or operand == 'G':
                    users = o_t.to.split(',')
                    decoded_message.text = o_t.text
                    self.broadcast_message_to_users(users, decoded_message)
                    self.save_messages(username, users, decoded_message.date, decoded_message.text)

                if operand == 'B':
                    decoded_message.text = o_t.text
                    self.broadcast_message_to_users(ALL_USER.keys(), decoded_message)
                    self.save_messages(username, ALL_USER.keys(), decoded_message.date, decoded_message.text)

                if operand == 'M':
                    self.user_messages(username)

    @staticmethod
    def send_message(connection: socket, message: Message):
        connection.send(message.encoded_message())
        time.sleep(0.1)


server = Server()
