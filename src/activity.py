import json
from datetime import datetime

curr = datetime.now()


def tampil_menu_catat_pengeluaran(username):
    key = ''


nominalstr = ''
n = 0
status = 1
nominal = 0

menu.header_menu()
menu.text_menu("Nama  : " +)  # getNamaUser(Username))
menu.h_line()
menu.text_menu("Catat Pengeluaran")
menu.h_line()
menu.text_menu("Nominal ", end='')
# formatRupiah(nominal)
print()
menu.h_line()
menu.back_instruction()
core.goto_xy(13, 7)

while key != 27:
    key = msvcrt.getch()

    if key.isdigit() and n < 9:
        if not (n == 0 and key == b'0'):
            nominalstr += key.decode()
            n += 1
            nominal = int(nominalstr)

            core.goto_xy(11, 7)
            print("                  ", end='')
            core.gotoxy(11, 7)
            # format_rupiah(nominal)
            core.gotoxy(11 + '''getLengthFormatRupiah(nominal) + '''
            2, 7)

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
                # format_rupiah(nominal)
                core.goto_xy(11 + '''getLengthFormatRupiah(nominal) + '''
                2, 7)

            if key == 13:
            # tampil_pilih_kategori(username, 1, nominal)
            if key == 27:
        # tampil_menu_catat(username)

def record_income(username, id_wallet, category, amount):
    file_name = "data/data.json"

    try:
        with open(file_name, "r+") as file:
            data = json.load(file)
            for user in data:
                if user.get("username") == username:
                    wallets = user.get("wallet", [])
                    for wallet in wallets:
                        if wallet.get("id") == id_wallet:
                            activities = wallet.get("activity", [])
                            activity = {
                                "id": len(activities) + 1,
                                "waktu": str(curr),
                                "jenis": "Pemasukan",
                                "kategori": category,
                                "nominal": amount
                            }
                            activities.append(activity)
                            # Update balance
                            wallet["saldo"] += amount
                            file.seek(0)
                            json.dump(data, file, indent=4)
                            file.truncate()
                            print("Income activity recorded successfully.")
                            return
                    print("\nDompet dengan ID yang diberikan tidak ditemukan\n")
                    return
            print("\nUsername tidak ditemukan\n")
    except FileNotFoundError:
        print("\nGagal membuka file dompet\n")
    except json.JSONDecodeError:
        print("\nFile dompet tidak valid (JSON tidak valid)\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")


def record_outcome(username, id_wallet, category, amount):
    file_name = "data/data.json"

    try:
        with open(file_name, "r+") as file:
            data = json.load(file)
            for user in data:
                if user.get("username") == username:
                    wallets = user.get("wallet", [])
                    for wallet in wallets:
                        if wallet.get("id") == id_wallet:
                            activities = wallet.get("activity", [])
                            activity = {
                                "id": len(activities) + 1,
                                "waktu": str(curr),
                                "jenis": "Pengeluaran",
                                "kategori": category,
                                "nominal": amount
                            }
                            activities.append(activity)
                            # Update balance
                            wallet["saldo"] -= amount
                            file.seek(0)
                            json.dump(data, file, indent=4)
                            file.truncate()
                            print("Outcome activity recorded successfully.")
                            return
                    print("\nDompet dengan ID yang diberikan tidak ditemukan\n")
                    return
            print("\nUsername tidak ditemukan\n")
    except FileNotFoundError:
        print("\nGagal membuka file dompet\n")
    except json.JSONDecodeError:
        print("\nFile dompet tidak valid (JSON tidak valid)\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")