from src import core
from src import menu
import msvcrt


def login_menu():
    username = ""
    password = ""
    input_length = 0
    input_order = 1
    status = 1
    key = 0

    core.clear_screen()
    menu.header_menu()
    menu.text_menu("Silakan masuk ke akunmu")
    menu.h_line()

    while status == 1:
        core.goto_xy(0, 5)
        menu.text_menu("Username\t:                     ")
        menu.text_menu("Password\t:                     ")
        menu.back_instruction()
        core.goto_xy(18, 5)

        while True:
            key = ord(core.get_key())

            if core.check_key(key) and (input_length < 20):
                if input_order == 1:
                    username += chr(key)
                    print(f"\033[92m{chr(key)}\033[0m")
                else:
                    password += chr(key)
                    print("\033[92m*\033[0m")
                input_length += 1
                core.goto_xy(18 + input_length, 4 + input_order)
            elif key == 13:  # Enter key
                if input_length > 0:
                    if input_order == 1:
                        input_order = 2
                        input_length = 0
                        core.goto_xy(18 + input_length, 4 + input_order)
                    else:
                        input_order = 1
                        input_length = 0
                        break
            elif key == 8:  # Backspace key
                if input_length > 0:
                    print("\b \b")
                    input_length -= 1
                    if input_order == 1:
                        username = username[:-1]
                    else:
                        password = password[:-1]
                    core.goto_xy(18 + input_length, 4 + input_order)
            elif key == 27:  # ESC key
                status = 0
                break

        if key == 13:
            core.goto_xy(0, 7)
            status = login(username, password)
            core.get_key()
            username = ""
            password = ""
            menu.show_message("", 7)
            if status == 0:
                menu.home_menu(username)

    if key == 27:
        menu.first_menu()


def register_menu():
    name = ""
    username = ""
    password = ""
    re_password = ""
    input_length = 0
    input_order = 1
    status = 1
    key = 0

    core.clear_screen()
    menu.header_menu()
    menu.text_menu("Silakan buat akun baru")
    menu.h_line()

    while status == 1:
        core.goto_xy(0, 5)
        menu.text_menu("Nama\t\t\t:                     ")
        menu.text_menu("Username\t\t:                     ")
        menu.text_menu("Password\t\t:                     ")
        menu.text_menu("Ulangi Password\t:                     ")
        menu.back_instruction()
        core.goto_xy(26, 5)

        while True:
            key = ord(core.get_key())

            if core.check_key(key) and (input_length < 20):
                if input_order == 1:
                    name += chr(key)
                    print(f"\033[92m{chr(key)}\033[0m")
                elif input_order == 2:
                    username += chr(key)
                    print(f"\033[92m{chr(key)}\033[0m")
                elif input_order == 3:
                    password += chr(key)
                    print("\033[92m*\033[0m")
                else:
                    re_password += chr(key)
                    print("\033[92m*\033[0m")
                input_length += 1
                core.goto_xy(26 + input_length, 4 + input_order)
            elif key == 13:  # Enter key
                if input_length > 0:
                    if input_order == 1:
                        input_order = 2
                        input_length = 0
                        core.goto_xy(26 + input_length, 4 + input_order)
                    elif input_order == 2:
                        input_order = 3
                        input_length = 0
                        core.goto_xy(26 + input_length, 4 + input_order)
                    elif input_order == 3:
                        input_order = 4
                        input_length = 0
                        core.goto_xy(26 + input_length, 4 + input_order)
                    else:
                        input_order = 1
                        input_length = 0
                        break
            elif key == 8:  # Backspace key
                if input_length > 0:
                    print("\b \b")
                    input_length -= 1
                    if input_order == 1:
                        name = name[:-1]
                    elif input_order == 2:
                        username = username[:-1]
                    elif input_order == 3:
                        password = password[:-1]
                    else:
                        re_password = re_password[:-1]
                    core.goto_xy(26 + input_length, 4 + input_order)
            elif key == 27:  # ESC key
                status = 0
                break

        if key == 13:
            core.goto_xy(0, 9)
            status = register(name, username, password, re_password)
            core.get_key()
            name = ""
            username = ""
            password = ""
            re_password = ""
            menu.show_message("", 9)
            if status == 0:
                menu.home_menu(username)

    if key == 27:
        menu.first_menu()


def login(username, password):
    data = core.read_data()

    user_found = False
    for user in data:
        if user["username"] == username:
            if user["password"] == core.hash_password(password):
                menu.show_message("Berhasil login sebagai " + user["name"], 7, 0)
                return 0
            else:
                menu.show_message("Password salah, silakan coba lagi", 7, 1)
                return 1

    if not user_found:
        menu.show_message("Username tidak ditemukan", 7, 1)
        return 1


def register(name, username, password, re_password):
    data = core.read_data()

    for user in data:
        if user["username"] == username:
            menu.show_message("Username sudah digunakan", 9, 1)
            return 1

    if password == re_password:
        new_id = len(data) + 1
        user_data = {
            "id": new_id,
            "name": name,
            "username": username,
            "password": core.hash_password(password),
            "wallet": [
                {
                    "id": 1,
                    "wallet_name": "Dompet utama",
                    "balance": 0,
                    "activity": []
                }
            ]
        }
        data.append(user_data)
        core.write_data(data)
        menu.show_message("Registrasi berhasil!", 9, 0)
        return 0
    else:
        core.goto_xy(0, 9)
        menu.clear_message()
        core.goto_xy(0, 9)
        menu.show_message("Password dan Ulangi Password tidak sama", 9, 1)
        return 1

def get_acc_name(username):
    file_name = "data/data.json"

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            for user in data:
                if user['username'] == username:
                    return user['name']
    except FileNotFoundError:
        print(f"\nGagal membuka file {file_name}\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")
    
    print(f"\nNama Akun dengan username '{username}' tidak ditemukan\n")
    return None

def tampil_menu_catat_pengeluaran(username):
	key = ''
    nominalstr = ''
    n = 0
    status = 1
    nominal = 0
    
    menu.header_menu()
    menu.text_menu("Nama  : " + ) #getNamaUser(Username))
    menu.h_line()
    menu.text_menu("Catat Pengeluaran")
    menu.h_line()
    menu.text_menu("Nominal ", end='')
    #formatRupiah(nominal)
    print()
    menu.h_line()
    menu.back_instruction()
    core.goto_xy(13, 7)
    
    while key !=  27 :  
        key = msvcrt.getch()

        if key.isdigit() and n < 9:
            if not (n == 0 and key == b'0'):
                nominalstr += key.decode()
                n += 1
                nominal = int(nominalstr)

                core.goto_xy(11, 7)
                print("                  ", end='')
                core.gotoxy(11, 7)
                #format_rupiah(nominal)
                core.gotoxy(11 + '''getLengthFormatRupiah(nominal) + ''' 2, 7)

        elif key == 13:  # Enter key
            if n > 0:
                nominal = int(nominalstr)
                n = 0
                break

        elif key == 8:  # Backspace key
            if n > 0:
                n -= 1

                nominalstr = nominalstr[:-1]
                if nominalstr == '':
                    nominal = 0
                else:
                    nominal = int(nominalstr)

                core.goto_xy(11, 7)
                print("                  ", end='')
                core.goto_xy(11, 7)
                #format_rupiah(nominal)
                core.goto_xy(11 + '''getLengthFormatRupiah(nominal) + ''' 2, 7)

    if key == 13:
        #tampil_pilih_kategori(username, 1, nominal)
    if key == 27:
        #tampil_menu_catat(username)
