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
    
        
def format_rupiah(amount):
    return f"Rp{'{:,}'.format(amount).replace(',', '.')}"


def check_date(day, month, year):
    if month < 1 or month > 12:
        return 1

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_month[1] = 29

    if day < 1 or day > days_in_month[month - 1]:
        return 1

    return 0


def get_date(day=True, date=True, month=True, year=True):
    nama_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    nama_bulan = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    tanggal_saat_ini = datetime.datetime.now()
    hari = nama_hari[tanggal_saat_ini.weekday()]
    tanggal = tanggal_saat_ini.day
    bulan = nama_bulan[tanggal_saat_ini.month]
    tahun = tanggal_saat_ini.year

    result = ""
    if day:
        result += hari
    if date:
        if result:
            result += ", "
        result += str(tanggal)
    if month:
        if result:
            result += " "
        result += bulan
    if year:
        if result:
            result += " "
        result += str(tahun)

    return result.strip()


def format_date(number):
    date_str = str(number)
    length = len(date_str)
    day = date_str[:2] if length >= 2 else date_str.ljust(2, '0')
    month = date_str[2:4] if length >= 4 else date_str[2:].ljust(2, '0')
    year = date_str[4:].ljust(4, '0')
    return f"{day}/{month}/{year}"


def format_date_2(number, displayDay=True):
    day = int(number[:2])
    month = int(number[2:4])
    year = int(number[4:])
    days_of_week = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    day_of_week = days_of_week[datetime.datetime(year, month, day).weekday()]
    months = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    month_name = months[month]
    if displayDay is True:
        formatted_date = f"{day_of_week}, {day} {month_name} {year}"
    else:
        formatted_date = f"{month_name} {year}"
    return formatted_date


def check_time(hour, minute):
    if 0 <= int(hour) <= 23 and 0 <= int(minute) <= 59:
        return 0
    else:
        return 1


def format_time(number):
    time_str = str(number)
    time_str = time_str.ljust(4, '0')
    hour = int(time_str[:2])
    minute = int(time_str[2:])
    formatted_time = f"{hour:02d}:{minute:02d}"
    return formatted_time
