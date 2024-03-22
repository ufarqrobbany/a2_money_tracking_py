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
    menu.text_menu(f"Saldo Awal\t\t: {core.format_rupiah(int(first_balance))}")

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
    jml_dompet = 0
    initiate = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu("Nama : ")
    menu.h_line()
    menu.text_menu("Pilih dompet yang akan diubah namanya")
    menu.h_line()

    # hitung dompet
    jml_dompet = get_dompet(username, False)

    dom = None
    file_name = "data\\wallets\\wallet_%s.dat" % username

    with open(file_name, "rb") as file:
        while True:
            id_kosong = []
            kosong = 0
            os.system("cls" if os.name == "nt" else "clear")

            if initiate == 1:
                print("[%c] " % chr(254))

            while True:
                data = file.read(sizeof(struct Wallet))
                if not data:
                    break
                dom = struct.unpack("20s f", data)
                if dom[0].strip() != "":
                    if initiate == 1:
                        print("[%c] %s, " % (chr(254), dom[0].strip()))
                    else:
                        print("[%c] %s, " % (chr(254) if current_selection == dom[1] or initiate == 1 else ' ', dom[0].strip()))
                    format_rupiah(dom[1])
                    print("\n")
                    j += 1
                    if current_selection == dom[1] and is_id_in_kosong(current_selection, id_kosong, kosong):
                        current_selection = dom[1]
                    initiate += 1
                else:
                    id_kosong.append(dom[1])
                    kosong += 1

            if current_selection <= 0 or is_id_in_kosong(current_selection, id_kosong, kosong):
                for i in range(1, get_last_id_dompet(username) + 2):
                    if i not in id_kosong:
                        current_selection = i
                        break

            print("[\033[1;31m%c\033[0m] Kembali\n" % (chr(254) if current_selection == get_last_id_dompet(username) + 1 else ' '))
            print("===================================================\n")
            print("Gunakan tombol panah untuk navigasi dan tekan Enter")

            # navigasi menu
            key = input()

            initiate = 2
            file.seek(0)

            if key == 72 and current_selection > 1:
                while current_selection > 1:
                    current_selection -= 1
                    if not is_id_in_kosong(current_selection, id_kosong, kosong):
                        break
                if is_id_in_kosong(current_selection, id_kosong, kosong):
                    first_non_empty_id = get_first_non_empty_id(id_kosong, kosong, get_last_id_dompet(username))
                    if first_non_empty_id > 0:
                        current_selection = first_non_empty_id
                current_selection = 1 if current_selection < 1 else current_selection
            elif key == 80 and current_selection < get_last_id_dompet(username) + 1:
                while current_selection < get_last_id_dompet(username) + 1:
                    current_selection += 1
                    if not is_id_in_kosong(current_selection, id_kosong, kosong):
                        break
                if is_id_in_kosong(current_selection, id_kosong, kosong):
                    first_non_empty_id = get_first_non_empty_id(id_kosong, kosong, get_last_id_dompet(username))
                    if first_non_empty_id > 0:
                        current_selection = first_non_empty_id
                current_selection = get_last_id_dompet(username) + 1 if current_selection > get_last_id_dompet(username) + 1 else current_selection
            elif key == 13:
                file.close()
                if current_selection == get_last_id_dompet(username) + 1:
                    #tampil_menu_dompet(username)
                else:
                    #tampil_menu_input_nama_dompet(username, current_selection)

            if key == 13:
                break         

                
def change_wallet_name(username, wallet_id, new_name):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    wallet["wallet_name"] = new_name
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



def add_balance(username, wallet_id, nominal):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    if (wallet["balance"] + nominal) <= 999999999:
                        wallet["balance"] = wallet["balance"] + nominal
                        core.write_data(data)
                        return 0
                    else:
                        return 1


def reduce_balance(username, wallet_id, nominal):
    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    if (wallet["balance"] - nominal) >= 0:
                        wallet["balance"] = wallet["balance"] - nominal
                        core.write_data(data)
                        return 0
                    else:
                        return 1

