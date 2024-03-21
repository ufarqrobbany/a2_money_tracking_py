import os
import ctypes
import msvcrt
import json
import hashlib
import datetime

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


def check_date(day, month, year):
    if month < 1 or month > 12:
        return 1

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_month[1] = 29

    if day < 1 or day > days_in_month[month - 1]:
        return 1

    return 0

def getDate(D=False, d=False, m=False, y=False):
    # Daftar nama hari dalam Bahasa Indonesia
    nama_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

    # Daftar nama bulan dalam Bahasa Indonesia
    nama_bulan = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    # Mendapatkan tanggal saat ini
    tanggal_saat_ini = datetime.datetime.now()

    # Mendapatkan nama hari dalam Bahasa Indonesia
    hari = nama_hari[tanggal_saat_ini.weekday()]

    # Mendapatkan tanggal
    tanggal = tanggal_saat_ini.day

    # Mendapatkan nama bulan dalam Bahasa Indonesia
    bulan = nama_bulan[tanggal_saat_ini.month]

    # Mendapatkan tahun
    tahun = tanggal_saat_ini.year

    if D:
        return hari
    elif d:
        return tanggal
    elif m:
        return bulan
    elif y:
        return tahun
    else:
        return f"{hari}, {tanggal} {bulan} {tahun}"

