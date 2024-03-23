from src import core
from src import menu
from src import account
from src import wallet
from src.wallet import get_wallet_id
import datetime
from src import activity


def record_income_amount(username, amount):
    if amount == "0":
        input_length = 0
    else:
        input_length = len(amount)

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pemasukan (Masukkan Jumlah Pemasukan)")
    menu.h_line()
    menu.text_menu(f"Jumlah Pemasukan\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu("Kategori Pemasukan\t\t: ")
    menu.text_menu("Dompet Tujuan\t\t: ")
    menu.text_menu("Tanggal \t\t\t: ")
    menu.text_menu("Waktu \t\t\t: ")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.back_instruction()
    if amount == "0":
        core.goto_xy(36, 7)
    else:
        core.goto_xy(34 + len(core.format_rupiah(int(amount))), 7)

    while True:
        key = ord(core.get_key())

        if core.check_key(key, True) and (input_length < 9):
            amount += chr(key)
            input_length += 1
            core.goto_xy(34, 7)
            print("                          ")
            core.goto_xy(34, 7)
            print(f"\033[92m{core.format_rupiah(int(amount))}\033[0m")
            core.goto_xy(34 + len(core.format_rupiah(int(amount))), 7)
        elif key == 13:
            if input_length > 0:
                input_length = 0
                break
        elif key == 8:
            if input_length > 0 and amount != "0":
                input_length -= 1
                amount = amount[:-1]
                core.goto_xy(34, 7)
                print("                          ")
                core.goto_xy(34, 7)
                print(f"\033[92m{core.format_rupiah(int(amount))}\033[0m")
                core.goto_xy(34 + len(core.format_rupiah(int(amount))), 7)
        elif key == 27:
            menu.home_menu(username)
            break

    if key == 13:
        record_income_select_category(username, amount)


def record_income_select_category(username, amount):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pemasukan")
    menu.h_line()
    menu.text_menu(f"Jumlah Pemasukan\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu("Kategori Pemasukan\t\t: ")
    menu.text_menu("Dompet Tujuan\t\t: ")
    menu.text_menu("Tanggal \t\t\t: ")
    menu.text_menu("Waktu \t\t\t: ")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.h_line()
    menu.text_menu("Pilih Kategori Pemasukan")
    menu.h_line()

    data = activity.get_category(username, "Pemasukan")
    while True:
        total_category = 0
        core.goto_xy(0, 16)
        menu.option("Tambah Kategori Baru", current_selection, 1)
        for index, category in enumerate(data):
            menu.option(f"\033[95m{category}\033[0m", current_selection, index + 2)
            total_category += 1
        menu.option("Kembali", current_selection, total_category + 2, True)
        menu.nav_instruction()
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < total_category + 2:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                record_income_category(username, amount)
            elif current_selection <= total_category + 1:
                record_income_select_wallet(username, amount, data[current_selection - 2])
            elif current_selection == total_category + 2:
                record_income_amount(username, amount)
            break

