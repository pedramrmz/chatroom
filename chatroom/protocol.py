from datetime import datetime


class Message:
    spliter = '<>'

    def __init__(self, date, text, username=None):
        self.username = username
        self.date = date
        self.text = text
        self.str_to_datetime()

    def encoded_message(self):
        message = str(self.datetime_to_str() + self.spliter + self.text)
        if self.username:
            message += self.spliter + self.username
        return message.encode()

    def datetime_to_str(self):
        return self.date.strftime("%Y-%m-%d %H:%M:%S")

    def str_to_datetime(self):
        if type(self.date) != datetime:
            self.date = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def decode_message(message, username=None):
        if len(message) <= 1:
            return False

        decoded_message = str(message.decode()).split(Message.spliter)
        message = Message(*decoded_message)
        if username:
            message.username = username
        return message

    def print_message(self):
        print(f'{self.date.strftime("%H:%M")} {self.username}: {self.text}')


class OperandText:
    spliter = '<O>'

    def __init__(self, operand, text=None, to=None):
        self.operand = operand
        self.to = to
        self.text = text

    def create_text(self):
        message = self.operand
        if self.text:
            message += self.spliter + self.text
        if self.to:
            message += self.spliter + self.to
        return message

    @staticmethod
    def get_text(text):
        operand_text = text.split(OperandText.spliter)
        operand_text_obj = OperandText(*operand_text)
        return operand_text_obj


class SaveMessage:
    spliter = ' '

    def __init__(self, fr, to, date, text):
        self.fr = fr
        self.to = to
        self.date = date
        self.text = text

    def convert_to_string(self):
        return str(self.fr + ' --> ' + self.to + ':' + self.spliter + self.text)


def encrypt_string(text, key):
    encrypted = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char) - ascii_offset + key) % 26 + ascii_offset)
            encrypted += encrypted_char
        else:
            encrypted += char
    return encrypted


def decrypt_string(encrypted_text, key):
    decrypted = ""
    for char in encrypted_text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            decrypted_char = chr((ord(char) - ascii_offset - key) % 26 + ascii_offset)
            decrypted += decrypted_char
        else:
            decrypted += char
    return decrypted