TCP_HOST = '127.0.0.1'
TCP_PORT = 12338
MESSAGE_MAX_LENGTH = 2048
SERVER_MAX_CONNECTION = 100
SERVER_USERNAME = 'SERVER'
GET_USERNAME_TEXT = 'ENTER USERNAME: '
GET_NEW_PASSWORD_TEXT = 'ENTER NEW PASSWORD: '
GET_PASSWORD_TEXT = 'ENTER PASSWORD: '
WRONG_PASSWORD = 'WRONG PASSWORD.'
ANOTHER_ACCOUNT_ALREADY_ONLINE = 'ANOTHER_ACCOUNT_ALREADY_ONLINE'
WELCOME_MESSAGE = 'WELCOME. KEYWORD: \nM -> get all message\nP -> private chat\nG -> group chat\nB -> broadcast.\nMode -> Change mode(Available, Busy)'
BUSY_MODE = 'CANT SEND MESSAGE IN BUSY MODE'
CHANGE_MODE_TO_BUSY = 'CHANGE_MODE_TO_BUSY'
CHANGE_MODE_TO_AVAILABLE = 'CHANGE_MODE_TO_AVAILABLE'
ENCRYPT_KEY = 123
class UserCondition:
    online = 'online'
    offline = 'offline'


class UserMode:
    available = 'available'
    busy = 'busy'
