import os
import ctypes
import msvcrt
import json
import hashlib

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# GOTO XY reference: https://stackoverflow.com/questions/21330632/pythonic-alternative-of-gotoxy-c-code
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    def __init__(self, x, y):
        self.X = x
        self.Y = y


def goto_xy(x, y):
    INIT_POS = COORD(x, y)
    STD_OUTPUT_HANDLE = -11
    hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetConsoleCursorPosition(hOut, INIT_POS)


def check_key(key, number_only=False):
    if number_only:
        return 48 <= key <= 57
    else:
        return (65 <= key <= 90) or (97 <= key <= 122) or (48 <= key <= 57) or (key == 32)


def get_key():
    return msvcrt.getch()


def read_data():
    if os.path.exists('data/data.json'):
        with open('data/data.json', 'r') as file:
            return json.load(file)
    else:
        return []


def write_data(data):
    with open('data/data.json', 'w') as file:
        json.dump(data, file)


def hash_password(password):
    password_bytes = password.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(password_bytes)
    encrypted_password = sha256.hexdigest()
    return encrypted_password
    
        
def format_rupiah(nominal):
    return f"Rp{'{:,}'.format(nominal).replace(',', '.')},00"
