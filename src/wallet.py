from src import core
from src import menu
from src import account


def wallet_menu(username):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : {account.get_account_name(username)}")
    menu.h_line()
    total_wallet = get_total_wallet(username)
    display_wallet(username)
    menu.h_line()

    while True:
        core.goto_xy(0, 4 + total_wallet + 3)
        menu.option("Tambah Dompet", current_selection, 1)
        menu.option("Ubah Nama Dompet", current_selection, 2)
        menu.option("Hapus Dompet", current_selection, 3)
        menu.option("Kembali", current_selection, 4, True)
        menu.nav_instruction()

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 4:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                if total_wallet < 10:
                    add_wallet_menu(username)
                else:
                    menu.show_message("Tidak bisa menambah dompet, maksimal 10 dompet", 11 + total_wallet, True)
                    core.get_key()
            elif current_selection == 2:
                change_wallet_name_menu(username)
            elif current_selection == 3:
                if total_wallet > 1:
                    # tampil_menu_hapus_dompet(username)
                    pass
                else:
                    menu.show_message("Tidak bisa menghapus dompet, sisakan 1 dompet di akunmu", 11 + total_wallet, True)
                    core.get_key()
            elif current_selection == 4:
                menu.home_menu(username)
            break


def add_wallet_menu(username):
    wallet_name = ""
    first_balance = "0"
    total_wallet = get_total_wallet(username)
    input_length = 0
    input_order = 1
    status = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : {account.get_account_name(username)}")
    menu.h_line()
    display_wallet(username)
    menu.h_line()
    menu.text_menu("Tambah Dompet Baru")
    menu.h_line()
    menu.text_menu("Nama Dompet Baru\t:")
    menu.text_menu(f"Saldo Awal\t\t: \033[92m{core.format_rupiah(int(first_balance))}\033[0m")

    while status == 1:
        core.goto_xy(0, 11 + total_wallet)
        menu.back_instruction()
        core.goto_xy(26, 4 + total_wallet + 5)

        while True:
            key = ord(core.get_key())
            if core.check_key(key) and (input_length < 20):
                if input_order == 1:
                    wallet_name += chr(key)
                    print(f"\033[92m{chr(key)}\033[0m")
                    input_length += 1
                    core.goto_xy(26 + input_length, 8 + input_order + total_wallet)
                elif (input_order == 2) and core.check_key(key, True) and (input_length < 9):
                    first_balance += chr(key)
                    input_length += 1
                    core.goto_xy(26, 8 + input_order + total_wallet)
                    print("                     ")
                    core.goto_xy(26, 8 + input_order + total_wallet)
                    print(f"\033[92m{core.format_rupiah(int(first_balance))}\033[0m")
                    core.goto_xy(26 + len(core.format_rupiah(int(first_balance))), 8 + input_order + total_wallet)
            elif key == 13:
                if input_length == 0 and input_order == 2:
                    first_balance = "0"
                    input_order = 1
                    input_length = 0
                    break
                if input_length > 0:
                    if input_order == 1:
                        input_order = 2
                        input_length = 0
                        core.goto_xy(26 + input_length + 2, 8 + input_order + total_wallet)
                    else:
                        input_order = 1
                        input_length = 0
                        break
            elif key == 8:
                if input_length > 0:
                    if input_order == 1:
                        print("\b \b")
                        input_length -= 1
                        wallet_name = wallet_name[:-1]
                        core.goto_xy(26 + input_length, 8 + input_order + total_wallet)
                    if input_order == 2:
                        input_length -= 1
                        first_balance = first_balance[:-1]
                        core.goto_xy(26, 8 + input_order + total_wallet)
                        print("                     ")
                        core.goto_xy(26, 8 + input_order + total_wallet)
                        print(f"\033[92m{core.format_rupiah(int(first_balance))}\033[0m")
                        core.goto_xy(26 + len(core.format_rupiah(int(first_balance))), 8 + input_order + total_wallet)
            elif key == 27:
                break

        if key == 13:
            status = add_wallet(username, wallet_name, int(first_balance))
            if status == 1:
                menu.show_message("Nama dompet sudah ada", 11 + total_wallet, status)
                core.get_key()
                first_balance = "0"
                wallet_name = ""
                core.goto_xy(26, 8 + input_order + total_wallet)
                print("                     ")
                core.goto_xy(26, 9 + input_order + total_wallet)
                print("                     ")
                core.goto_xy(26, 9 + input_order + total_wallet)
                print(f"\033[92m{core.format_rupiah(int(first_balance))}\033[0m")
                core.goto_xy(26 + len(core.format_rupiah(int(first_balance))), 8 + input_order + total_wallet)
            else:
                menu.show_message("Berhasil menambah dompet baru", 11 + total_wallet, status)
                core.get_key()
                wallet_menu(username)
                break

        if key == 27 or status == 0:
            wallet_menu(username)
            break


def add_wallet(username, wallet_name, first_balance):
    data = core.read_data()

    new_wallet = {
        "id": get_last_wallet_id(username) + 1,
        "wallet_name": wallet_name,
        "balance": first_balance,
        "activity": []
    }

    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["wallet_name"] == wallet_name:
                    return 1
            user["wallet"].append(new_wallet)
            core.write_data(data)
            return 0


def change_wallet_name_menu(username):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : {account.get_account_name(username)}")
    menu.h_line()
    menu.text_menu("Pilih dompet yang akan diubah namanya")
    menu.h_line()

    data = core.read_data()
    for user in data:
        if user["username"] == username:
            while True:
                total_wallet = 0
                core.goto_xy(0, 7)
                for index, wallet in enumerate(user["wallet"]):
                    menu.option(f"{wallet["wallet_name"]}, {core.format_rupiah(wallet['balance'])}", current_selection, index + 1)
                    total_wallet += 1

                menu.option("Kembali", current_selection, total_wallet + 1, True)
                menu.nav_instruction()
                core.goto_xy(0, 0)

                key = ord(core.get_key())

                if key == 72 and current_selection > 1:
                    current_selection -= 1
                elif key == 80 and current_selection < total_wallet + 1:
                    current_selection += 1
                elif key == 13:
                    if current_selection <= total_wallet:
                        wallet_id = get_wallet_id(username, current_selection - 1)
                        change_wallet_name_input(username, wallet_id)
                    elif current_selection == total_wallet + 1:
                        wallet_menu(username)
                    break
                    

def change_wallet_name_input(username, wallet_id):
    new_name = ""
    input_length = 0
    status = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : {account.get_account_name(username)}")
    menu.h_line()
    menu.text_menu(f"Ubah Nama Dompet : {get_wallet_name(username, wallet_id)}")
    menu.h_line()
    menu.text_menu("Nama Baru\t:")

    while status == 1:
        core.goto_xy(0, 8)
        menu.back_instruction()
        core.goto_xy(18, 7)

        while True:
            key = ord(core.get_key())
            if core.check_key(key) and (input_length < 20):
                new_name += chr(key)
                print(f"\033[92m{chr(key)}\033[0m")
                input_length += 1
                core.goto_xy(18 + input_length, 7)
            elif key == 13:
                if input_length > 0:
                    input_length = 0
                    break
            elif key == 8:
                if input_length > 0:
                    print("\b \b")
                    input_length -= 1
                    new_name = new_name[:-1]
                    core.goto_xy(18 + input_length, 7)
            elif key == 27:
                break

        if key == 13:
            status = change_wallet_name(username, wallet_id, new_name)
            if status == 1:
                menu.show_message("Nama dompet sudah ada", 8, status)
                core.get_key()
                new_name = ""
                core.goto_xy(18, 7)
                print("                     ")
                core.goto_xy(18, 7)
            else:
                menu.show_message("Berhasil mengubah nama dompet", 8, status)
                core.get_key()
                wallet_menu(username)
                break

        if key == 27 or status == 0:
            change_wallet_name_menu(username)
            break
                
              
def change_wallet_name(username, wallet_id, new_name):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["wallet_name"] == new_name:
                    return 1
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    wallet["wallet_name"] = new_name
                    core.write_data(data)
                    return 0
            return 1


def delete_wallet_menu(username):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : {account.get_account_name(username)}")
    menu.h_line()
    menu.text_menu("Pilih dompet yang akan dihapus")
    menu.h_line()

    data = core.read_data()
    for user in data:
        if user["username"] == username:
            while True:
                total_wallet = 0
                core.goto_xy(0, 7)
                for index, wallet in enumerate(user["wallet"]):
                    menu.option(f"{wallet["wallet_name"]}, {core.format_rupiah(wallet['balance'])}", current_selection, index + 1)
                    total_wallet += 1

                menu.option("Kembali", current_selection, total_wallet + 1, True)
                menu.nav_instruction()
                core.goto_xy(0, 0)

                key = ord(core.get_key())

                if key == 72 and current_selection > 1:
                    current_selection -= 1
                elif key == 80 and current_selection < total_wallet + 1:
                    current_selection += 1
                elif key == 13:
                    if current_selection <= total_wallet:
                        wallet_id = get_wallet_id(username, current_selection - 1)
                        delete_wallet_confirm_menu(username, wallet_id)
                    elif current_selection == total_wallet + 1:
                        wallet_menu(username)
                    break

                    
def delete_wallet_confirm_menu(username, wallet_id):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : {account.get_account_name(username)}")
    menu.h_line()
    menu.text_menu(f"Konfirmasi Hapus Dompet {get_wallet_name(username, wallet_id)}")
    menu.text_menu("Semua riwayat aktivitas pada dompet ini akan terhapus")
    menu.h_line()

    while True:
        core.goto_xy(0, 8)
        menu.option("Tidak, kembali", current_selection, 1)
        menu.option("Hapus", current_selection, 2, True)
        menu.nav_instruction()
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 2:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                delete_wallet_menu(username)
            elif current_selection == 2:
                status = delete_wallet(username, wallet_id)
                if status == 0:
                    menu.show_message("Dompet berhasil dihapus", 10, status)
                core.get_key()
                wallet_menu(username)
            break      
            
            
def delete_wallet(username, wallet_id):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    user["wallet"].remove(wallet)
                    core.write_data(data)
                    return 0
            return 1
          
          
def display_wallet(username):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            menu.text_menu("List Dompet :")
            for wallet in user["wallet"]:
                menu.text_menu(f"○ {wallet["wallet_name"]}, {core.format_rupiah(wallet['balance'])}")


def get_total_wallet(username):
    data = core.read_data()
    total_wallet = 0
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                total_wallet += 1

    return total_wallet

          
def get_wallet_id(username, index):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for i, wallet in enumerate(user["wallet"]):
                if i == index:
                    return wallet["id"]


def get_wallet_name(username, wallet_id):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    return wallet["wallet_name"]

    print(f"Dompet dengan ID '{wallet_id}' tidak ditemukan")
    return None


def get_total_balance(username):
    data = core.read_data()
    total_balance = 0
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                total_balance += wallet["balance"]

    return total_balance


def get_wallet_balance(username, wallet_id):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    return wallet["balance"]

    print(f"Dompet dengan ID '{wallet_id}' tidak ditemukan untuk pengguna '{username}'")
    return -1


def get_last_wallet_id(username):
    data = core.read_data()
    wallet_id = 0
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                wallet_id = wallet["id"]

    return wallet_id


def add_balance(username, wallet_id, amount):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    if (wallet["balance"] + amount) <= 999999999:
                        wallet["balance"] = wallet["balance"] + amount
                        core.write_data(data)
                        return 0
                    else:
                        return 1


def reduce_balance(username, wallet_id, amount):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    if (wallet["balance"] - amount) >= 0:
                        wallet["balance"] = wallet["balance"] - amount
                        core.write_data(data)
                        return 0
                    else:
                        return 1

                      