import menu
import core
import json

def wallet_menu(username):
    current_selection = 1
    jml_dompet = 0
    key = ""

    core.clear_screen()
    # print header
    menu.header_menu()
    menu.h_line()
    menu.text_menu("Nama : ")
    menu.h_line()

    # tampil dompet
    # jml_dompet = get_dompet(username, True)
    menu.h_line()
    core.gotoxy(1, 10 + jml_dompet)

    # isi
    while True:
        core.gotoxy(1, 4)
        # gotoxy(1, 4 + jml_dompet + 3)
        menu.option("Tambah Dompet", current_selection, 1)
        menu.option("Ubah Nama Dompet", current_selection, 2)
        menu.option("Hapus Dompet", current_selection, 3)
        menu.option("Kembali", current_selection, 4 , True)
        
        menu.h_line()
        print("Gunakan tombol panah untuk navigasi dan tekan Enter")

        # navigasi menu
        key = ord(core.get_key())
        
        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 4:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                if jml_dompet < 10:
                    # tampil_menu_tambah_dompet(username)
                else:
                    core.gotoxy(1, 12 + jml_dompet)
                    print("Tidak bisa menambah dompet, maksimal 10 dompet dalam 1 akun")
                    core.get_key()
            elif current_selection == 2:
                # tampil_menu_ubah_nama_dompet(username)
            elif current_selection == 3:
                if jml_dompet > 1:
                    # tampil_menu_hapus_dompet(username)
                else:
                    core.gotoxy(1, 12 + jml_dompet)
                    print("Tidak bisa menghapus dompet lagi, sisakan 1 dompet di akunmu")
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