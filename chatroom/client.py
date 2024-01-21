import socket
import threading
from datetime import datetime

from protocol import Message, OperandText
from constants import *

LOST_CONNECTION = False


class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((TCP_HOST, TCP_PORT))
        except:
            print("Couldn't connect to server")

        self.create_connection()

    def create_connection(self):
        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()

    def handle_messages(self):
        while True:
            recv = self.socket.recv(MESSAGE_MAX_LENGTH)
            if recv and recv.decode() == 'heartbeat':
                continue
            message = Message.decode_message(recv)
            if message is False:
                print('CONNECTION LOST')
                exit(0)
            message.print_message()

    def input_handler(self):
        while True:
            text = input()
            if text == 'Mode':
                mode = input('Mode: Enter A(available) or B(busy): ')
                o_t = OperandText(text, text, mode)
                text = o_t.create_text()
            if text == 'P' or text == 'G':
                users = input('To: ')
                text_message = input('Text: ')
                o_t = OperandText(text, text_message, users)
                text = o_t.create_text()
            elif text == 'B':
                text_message = input('Text: ')
                o_t = OperandText(text, text_message)
                text = o_t.create_text()
            elif text == 'M':
                o_t = OperandText(text)
                text = o_t.create_text()
            current_date = datetime.now()
            message = Message(current_date, text)
            self.socket.send(message.encoded_message())


client = Client()
