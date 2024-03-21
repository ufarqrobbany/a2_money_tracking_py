from src import core
from src import menu


def wallet_menu(username):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu("Nama : ")
    menu.h_line()
    total_wallet = 0
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
                    # tampil_menu_tambah_dompet(username)
                    pass
                else:
                    menu.show_message("Tidak bisa menambah dompet, maksimal 10 dompet", 12 + total_wallet, True)
                    core.get_key()
            elif current_selection == 2:
                # tampil_menu_ubah_nama_dompet(username)
                pass
            elif current_selection == 3:
                if total_wallet > 1:
                    # tampil_menu_hapus_dompet(username)
                    pass
                else:
                    menu.show_message("Tidak bisa menghapus dompet, sisakan 1 dompet di akunmu", 12 + total_wallet, True)
                    core.get_key()
            elif current_selection == 4:
                menu.home_menu(username)
            break

        
def get_wallet_balance(username, id_dompet):
    file_name = f"data/data.json"

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            for user_data in data:
                if user_data.get("username") == username:
                    wallets = user_data.get("wallet", [])
                    for wallet_data in wallets:
                        if wallet_data.get("id") == id_dompet:
                            return wallet_data.get("saldo")
    except FileNotFoundError:
        print("\nGagal membuka file dompet\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")
    
    print(f"\nDompet dengan ID '{id_dompet}' tidak ditemukan untuk pengguna '{username}'\n")
    return -1

def get_wallet(username, display):
    file_name = f"data/data.json"

    n = 0

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            for user_data in data:
                if user_data.get("username") == username:
                    wallets = user_data.get("wallet", [])
                    if display:
                        print("Daftar dompet:")
                    for wallet_data in wallets:
                        wallet_nama_dompet = wallet_data.get("nama_dompet")
                        saldo = wallet_data.get("saldo")
                        if wallet_nama_dompet.strip() != "":
                            if display:
                                print(f"- {wallet_nama_dompet}, {saldo}")
                            n += 1
    except FileNotFoundError:
        print("\nGagal membuka file\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")

    return n

def get_wallet_name(username, id_dompet):
    file_name = f"data/data.json"

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            for user in data:
                if user['username'] == username:
                    for wallet in user['wallet']:
                        if wallet['id'] == id_dompet:
                            return wallet['nama_dompet']
    except FileNotFoundError:
        print(f"\nGagal membuka file dompet {file_name}\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")
    
    print(f"\nDompet dengan ID '{id_dompet}' tidak ditemukan\n")
    return None


def newDompet(nama_dompet, saldo_awal):
    dataBaru = {
        "id": 1,
        "nama_dompet": nama_dompet,
        "saldo": saldo_awal,
        "actitivy": []
    }
    return [dataBaru]

def tambahDompet(username, nama_dompet, saldo_awal):
    data = core.read_data()
    found = False
    index = None
    for i in range(len(data)):
        if data[i]['username'] == username:
            found = True
            index = i
            break
    if found:
        data[index]['wallet'].append(newDompet(nama_dompet, saldo_awal))
        core.write_data(data)
        return 0
    else:
        return 1

def add_wallet_menu(username):
    nama_dompet = ""
    saldo_awal = ""
    key = ''
    jml_dompet = 0
    n = 0
    p = 1
    status = 1
    saldo = 0

    while status == 1:
        core.clear_screen()

        # Print header
        menu.header_menu()
        menu.text_menu("Nama :")
        menu.h_line()
        menu.text_menu("Tambah dompet baru")
        menu.h_line()

        #jml_dompet = get_dompet(username, True)

        menu.h_line()
        menu.text_menu("Nama Dompet\t: ")
        menu.text_menu("Saldo Awal\t: ", end='')
        #format_rupiah(saldo)
        menu.back_instruction()
        core.goto_xy(19, 4 + jml_dompet + 5)

        while True:
            key = ord(core.get_key())
            if (key.isalnum() or key.isdigit() or key == ' ' or (n<20)):
                if (p == 1):
                    nama_dompet = key
                    n += 1
                    print(key)
                    core.goto_xy(19 + n, 8 + p + jml_dompet)
                elif ((p == 2) and (key >= '0' and key <= '9') and (n < 8)):
                    saldo_awal[n] = key
                    n += 1
                    saldo = int(''.join(saldoawal))
                    core.goto_xy(19, 8 + p + jml_dompet)
                    print("                  ", end='')
                    core.goto_xy(19, 8 + p + jml_dompet)
                    #format_rupiah(saldo)
                    #core.goto_xy(19 + get_length_format_rupiah(saldo) + 2, 8 + p + jml_dompet)
            elif key == 13:
                if n == 0 and p == 2:
                    saldo = 0
                    p = 1
                    n = 0
                    break
                if n > 0:
                    if p == 1:
                        nama_dompet[n] = '\0'
                        p = 2
                        n = 0
                        core.goto_xy(19 + n + 2, 8 + p + jml_dompet)
                    else:
                        saldoawal[n] = '\0'
                        saldo = int(''.join(saldoawal))
                        p = 1
                        n = 0
                        break
            elif key == 8:
                if n > 0:
                    if p == 1:
                        print("\b \b", end='', flush=True)
                    n -= 1
                    if p == 2:
                        saldoawal[n] = '\0'
                        saldo = int(''.join(saldoawal)) if saldoawal[0] else 0
                        core.goto_xy(19, 5 + p + jml_dompet)
                        print("                  ", end='')
                        core.goto_xy(19, 5 + p + jml_dompet)
                        #format_rupiah(saldo)
                        #core.goto_xy(19 + get_length_format_rupiah(saldo) + 2, 5 + p + jml_dompet)
            elif key == 27:
                break

        if key == 13:
            core.goto_xy(1, 9 + 2 + jml_dompet)
            #status = tambah_dompet(username, nama_dompet, saldo)
            input()

            if status == 1:
                saldoawal = [' '] * 9
                saldo = 0

                core.goto_xy(19, 5 + p + jml_dompet)
                print("                  ", end='')
                core.goto_xy(19, 5 + p + jml_dompet)
                #format_rupiah(saldo)
                #core.goto_xy(19 + get_length_format_rupiah(saldo) + 2, 5 + p + jml_dompet)

        if key == 27 or status == 0:
            break

    if status == 0:
        print()
        #tampil_menu_dompet(username)


def get_last_dompet(username):
    file_name = f"data/data.json"
    id_dompet = 0

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            for user in data:
                if user['username'] == username:
                    for wallet in user['wallet']:
                        id_dompet = wallet['id']
        return id_dompet
    except FileNotFoundError:
        print(f"\nGagal membuka file dompet {file_name}\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")

    
def add_balance(username, id_dompet, nominal):
    file_name = "data/data.json"

    try:
        with open(file_name, "r+") as file:
            data = json.load(file)
            for user in data:
                if user.get("username") == username:
                    wallets = user.get("wallet", [])
                    for wallet in wallets:
                        if wallet.get("id") == id_dompet:
                            saldo = wallet.get("saldo")
                            if saldo is not None:
                                new_saldo = saldo + nominal
                                wallet["saldo"] = new_saldo
                                file.seek(0)
                                json.dump(data, file, indent=4)
                                file.truncate()
                                return
                            else:
                                print("\nSaldo tidak ditemukan untuk dompet tersebut\n")
                                return
                    print("\nDompet dengan ID yang diberikan tidak ditemukan\n")
                    return
            print("\nUsername tidak ditemukan\n")
    except FileNotFoundError:
        print("\nGagal membuka file dompet\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")

def reduce_balance(username, id_dompet, nominal):
    file_name = "data/data.json"

    try:
        with open(file_name, "r+") as file:
            data = json.load(file)
            for user in data:
                if user.get("username") == username:
                    wallets = user.get("wallet", [])
                    for wallet in wallets:
                        if wallet.get("id") == id_dompet:
                            saldo = wallet.get("saldo")
                            if saldo is not None:
                                new_saldo = saldo - nominal
                                wallet["saldo"] = new_saldo
                                file.seek(0)
                                json.dump(data, file, indent=4)
                                file.truncate()
                                return
                            else:
                                print("\nSaldo tidak ditemukan untuk dompet tersebut\n")
                                return
                    print("\nDompet dengan ID yang diberikan tidak ditemukan\n")
                    return
            print("\nUsername tidak ditemukan\n")
    except FileNotFoundError:
        print("\nGagal membuka file dompet\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")

def change_wallet_name(username, id_dompet, newName):
    file_name = f"data/data.json"

    try:
        with open(file_name, "r+") as file:
            data = json.load(file)
            for user in data:
                if user['username'] == username:
                    for wallet in user['wallet']:
                        if wallet['id'] == id_dompet:
                            wallet['nama_dompet'] = newName
                            file.seek(0)
                            json.dump(data, file, indent=4)
                            file.truncate()
                            return
            print(f"\nDompet dengan ID '{id_dompet}' tidak ditemukan\n")
    except FileNotFoundError:
        print(f"\nGagal membuka file dompet {file_name}\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")