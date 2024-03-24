from src import core
from src import menu
from src import account
from src.wallet import *
from src import activity
import datetime


def record_transfer_source_wallet(username, date):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Transfer")
    menu.h_line()
    menu.text_menu("Dompet Asal\t\t\t: ")
    menu.text_menu("Dompet Tujuan\t\t: ")
    menu.text_menu(f"Jumlah Transfer\t\t: ")
    menu.text_menu(f"Tanggal \t\t\t: \033[92m{core.format_date_2(date)}\033[0m")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.h_line()
    menu.text_menu("Pilih Dompet Asal")
    menu.h_line()

    data = core.read_data()
    for user in data:
        if user["username"] == username:
            while True:
                total_wallet = 0
                core.goto_xy(0, 15)
                for index, wallet in enumerate(user["wallet"]):
                    menu.option(
                        f"\033[95m{wallet["wallet_name"]}\033[0m, \033[94m{core.format_rupiah(wallet['balance'])}\033[0m",
                        current_selection, index + 1)
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
                        record_transfer_destination_wallet(username, date, wallet_id)
                    elif current_selection == total_wallet + 1:
                        menu.home_menu(username)
                    break


def record_transfer_destination_wallet(username, date, source_wallet_id):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Transfer")
    menu.h_line()
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{get_wallet_name(username, source_wallet_id)}\033[0m")
    menu.text_menu("Dompet Tujuan\t\t: ")
    menu.text_menu(f"Jumlah Transfer\t\t: ")
    menu.text_menu(f"Tanggal \t\t\t: \033[92m{core.format_date_2(date)}\033[0m")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.h_line()
    menu.text_menu("Pilih Dompet Tujuan")
    menu.h_line()

    data = core.read_data()
    for user in data:
        if user["username"] == username:
            while True:
                total_wallet = 0
                core.goto_xy(0, 15)
                index = 0
                for wallet in user["wallet"]:
                    if wallet["id"] != source_wallet_id:
                        menu.option(
                            f"\033[95m{wallet["wallet_name"]}\033[0m, \033[94m{core.format_rupiah(wallet['balance'])}\033[0m",
                            current_selection, index + 1)
                        index += 1
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
                        wallet_id = get_wallet_id(username, current_selection - 1, source_wallet_id)
                        record_transfer_amount(username, date, source_wallet_id, wallet_id, "0")
                    elif current_selection == total_wallet + 1:
                        record_transfer_source_wallet(username, date)
                    break


def record_transfer_amount(username, date, source_wallet_id, destination_wallet_id, amount):
    if amount == "0":
        input_length = 0
    else:
        input_length = len(amount)

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Transfer (Masukkan Jumlah Transfer)")
    menu.h_line()
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{get_wallet_name(username, source_wallet_id)}\033[0m")
    menu.text_menu(f"Dompet Tujuan\t\t: \033[92m{get_wallet_name(username, destination_wallet_id)}\033[0m")
    menu.text_menu(f"Jumlah Transfer\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Tanggal \t\t\t: \033[92m{core.format_date_2(date)}\033[0m")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.back_instruction()
    if amount == "0":
        core.goto_xy(36, 9)
    else:
        core.goto_xy(34 + len(core.format_rupiah(int(amount))), 9)

    while True:
        key = ord(core.get_key())

        if core.check_key(key, True) and (input_length < 12):
            amount += chr(key)
            input_length += 1
            core.goto_xy(34, 9)
            print("                          ")
            core.goto_xy(34, 9)
            print(f"\033[92m{core.format_rupiah(int(amount))}\033[0m")
            core.goto_xy(34 + len(core.format_rupiah(int(amount))), 9)
        elif key == 13:
            if input_length > 0:
                input_length = 0
                break
        elif key == 8:
            if input_length > 0 and amount != "0":
                input_length -= 1
                amount = amount[:-1]
                core.goto_xy(34, 9)
                print("                          ")
                core.goto_xy(34, 9)
                print(f"\033[92m{core.format_rupiah(int(amount))}\033[0m")
                core.goto_xy(34 + len(core.format_rupiah(int(amount))), 9)
        elif key == 27:
            record_transfer_destination_wallet(username, date, source_wallet_id)
            break

    if key == 13:
        record_transfer_note(username, date, source_wallet_id, destination_wallet_id, amount)


def record_transfer_note(username, date, source_wallet_id, destination_wallet_id, amount):
    input_length = 0
    note = ""

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Transfer (Tambahkan Keterangan)")
    menu.h_line()
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{get_wallet_name(username, source_wallet_id)}\033[0m")
    menu.text_menu(f"Dompet Tujuan\t\t: \033[92m{get_wallet_name(username, destination_wallet_id)}\033[0m")
    menu.text_menu(f"Jumlah Transfer\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Tanggal \t\t\t: \033[92m{core.format_date_2(date)}\033[0m")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.back_instruction()
    core.goto_xy(34, 11)

    while True:
        key = ord(core.get_key())

        if core.check_key(key) and (input_length < 20):
            note += chr(key)
            print(f"\033[92m{chr(key)}\033[0m")
            input_length += 1
            core.goto_xy(34 + input_length, 11)
        elif key == 13:
            break
        elif key == 8:
            if input_length > 0:
                print("\b \b")
                input_length -= 1
                note = note[:-1]
                core.goto_xy(34 + input_length, 11)
        elif key == 27:
            record_transfer_amount(username, date, source_wallet_id, destination_wallet_id, amount)
            break

    if key == 13:
        record_income_confirm(username, date, source_wallet_id, destination_wallet_id, amount, note)
        pass


def record_income_confirm(username, date, source_wallet_id, destination_wallet_id, amount, note):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Transfer")
    menu.h_line()
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{get_wallet_name(username, source_wallet_id)}\033[0m")
    menu.text_menu(f"Dompet Tujuan\t\t: \033[92m{get_wallet_name(username, destination_wallet_id)}\033[0m")
    menu.text_menu(f"Jumlah Transfer\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Tanggal \t\t\t: \033[92m{core.format_date_2(date)}\033[0m")
    menu.text_menu(f"Keterangan (Opsional)\t: \033[92m{note}\033[0m")
    menu.h_line()
    menu.text_menu("Konfirmasi Transfer")
    balance = get_wallet_balance(username, source_wallet_id)
    menu.text_menu(f"\033[95m{get_wallet_name(username, source_wallet_id)}\033[0m : \033[94m{core.format_rupiah(balance)}\033[0m →  \033[94m{core.format_rupiah(balance - int(amount))}\033[0m")
    balance = get_wallet_balance(username, destination_wallet_id)
    menu.text_menu(f"\033[95m{get_wallet_name(username, destination_wallet_id)}\033[0m : \033[94m{core.format_rupiah(balance)}\033[0m →  \033[94m{core.format_rupiah(balance + int(amount))}\033[0m")
    menu.h_line()

    while True:
        core.goto_xy(0, 17)
        menu.option(f"Catat", current_selection, 1)
        menu.option("Kembali", current_selection, 2, True)
        menu.nav_instruction()
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 2:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                time = datetime.datetime.now().date().strftime('%H%M')
                status = activity.add_record(username, amount, "", source_wallet_id, date, time, note, "Transfer", destination_wallet_id)
                if status == 0:
                    menu.show_message("Berhasil mencatat transfer", 19, status)
                    core.get_key()
                    menu.home_menu(username)
                    break
                else:
                    menu.show_message("Saldo dompet asal kurang / saldo dompet tujuan melebihi batas", 19, status)
                    core.get_key()
            elif current_selection == 2:
                record_transfer_note(username, date, source_wallet_id, destination_wallet_id, amount)
                break

