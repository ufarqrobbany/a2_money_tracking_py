from src import core
from src import menu
from src import account
from src import wallet
from src.wallet import get_wallet_id
import datetime
from src import activity


def record_outcome_amount(username, amount):
    if amount == "0":
        input_length = 0
    else:
        input_length = len(amount)

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran (Masukkan Jumlah Pengeluaran)")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu("Kategori Pengeluaran\t\t: ")
    menu.text_menu("Dompet Asal\t\t\t: ")
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

        if core.check_key(key, True) and (input_length < 12):
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
        record_outcome_select_category(username, amount)


def record_outcome_select_category(username, amount):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu("Kategori Pengeluaran\t\t: ")
    menu.text_menu("Dompet Asal\t\t\t: ")
    menu.text_menu("Tanggal \t\t\t: ")
    menu.text_menu("Waktu \t\t\t: ")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.h_line()
    menu.text_menu("Pilih Kategori Pengeluaran")
    menu.h_line()

    data = activity.get_category(username, "Pengeluaran")
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
                record_outcome_category(username, amount)
            elif current_selection <= total_category + 1:
                record_outcome_select_wallet(username, amount, data[current_selection - 2])
            elif current_selection == total_category + 2:
                record_outcome_amount(username, amount)
            break


def record_outcome_category(username, amount):
    input_length = 0
    category = ""

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran (Masukkan Pengeluaran)")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu("Kategori Pengeluaran\t\t: ")
    menu.text_menu("Dompet Asal\t\t\t: ")
    menu.text_menu("Tanggal \t\t\t: ")
    menu.text_menu("Waktu \t\t\t: ")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.back_instruction()
    core.goto_xy(34, 8)

    while True:
        key = ord(core.get_key())

        if core.check_key(key) and (input_length < 20):
            category += chr(key)
            print(f"\033[92m{chr(key)}\033[0m")
            input_length += 1
            core.goto_xy(34 + input_length, 8)
        elif key == 13:
            if input_length > 0:
                input_length = 0
                break
        elif key == 8:
            if input_length > 0:
                print("\b \b")
                input_length -= 1
                category = category[:-1]
                core.goto_xy(34 + input_length, 8)
        elif key == 27:
            record_outcome_select_category(username, amount)
            break

    if key == 13:
        record_outcome_select_wallet(username, amount, category)


def record_outcome_select_wallet(username, amount, category):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Kategori Pengeluaran\t\t: \033[92m{category}\033[0m")
    menu.text_menu("Dompet Asal\t\t\t: ")
    menu.text_menu("Tanggal \t\t\t: ")
    menu.text_menu("Waktu \t\t\t: ")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.h_line()
    menu.text_menu("Pilih Dompet Asal")
    menu.h_line()

    data = core.read_data()
    for user in data:
        if user["username"] == username:
            while True:
                total_wallet = 0
                core.goto_xy(0, 16)
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
                        record_outcome_select_date(username, amount, category, wallet_id)
                    elif current_selection == total_wallet + 1:
                        record_outcome_select_category(username, amount)
                    break


def record_outcome_select_date(username, amount, category, wallet_id):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Kategori Pengeluaran\t\t: \033[92m{category}\033[0m")
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{wallet.get_wallet_name(username, wallet_id)}\033[0m")
    menu.text_menu("Tanggal \t\t\t: ")
    menu.text_menu("Waktu \t\t\t: ")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.h_line()
    menu.text_menu("Tentukan Tanggal")
    menu.h_line()

    while True:
        core.goto_xy(0, 16)
        menu.option(f"Hari Ini ({core.get_date()})", current_selection, 1)
        menu.option("Tanggal Lain", current_selection, 2)
        menu.option("Kembali", current_selection, 3, True)
        menu.nav_instruction()
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 3:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                record_outcome_time(username, amount, category, wallet_id, datetime.datetime.now().date().strftime('%d%m%Y'))
            elif current_selection == 2:
                record_outcome_date(username, amount, category, wallet_id)
            elif current_selection == 3:
                record_outcome_select_wallet(username, amount, category)
            break


def record_outcome_date(username, amount, category, wallet_id):
    input_length = 0
    date = "0"
    status = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran (Masukkan Tanggal/Bulan/Tahun)")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Kategori Pengeluaran\t\t: \033[92m{category}\033[0m")
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{wallet.get_wallet_name(username, wallet_id)}\033[0m")
    while status == 1:
        core.goto_xy(0, 10)
        menu.text_menu(f"Tanggal \t\t\t: {core.format_date(date)}")
        date = ""
        menu.text_menu("Waktu \t\t\t: ")
        menu.text_menu("Keterangan (Opsional)\t: ")
        menu.back_instruction()
        core.goto_xy(34, 10)

        while True:
            key = ord(core.get_key())

            if core.check_key(key, True) and (input_length < 8):
                date += chr(key)
                print(f"\033[92m{chr(key)}\033[0m")
                input_length += 1
                core.goto_xy(34, 10)
                print("                     ")
                core.goto_xy(34, 10)
                print(f"\033[92m{core.format_date(date)}\033[0m")
                if input_length < 2:
                    core.goto_xy(34 + input_length, 10)
                elif input_length < 4:
                    core.goto_xy(34 + input_length + 1, 10)
                elif input_length <= 8:
                    core.goto_xy(34 + input_length + 2, 10)
            elif key == 13:
                if input_length == 8:
                    input_length = 0
                    break
            elif key == 8:
                if input_length > 0:
                    input_length -= 1
                    date = date[:-1]
                    core.goto_xy(34, 10)
                    print("                     ")
                    core.goto_xy(34, 10)
                    if date == "":
                        print(f"\033[92m{core.format_date(0)}\033[0m")
                    else:
                        print(f"\033[92m{core.format_date(date)}\033[0m")
                    if input_length < 2:
                        core.goto_xy(34 + input_length, 10)
                    elif input_length < 4:
                        core.goto_xy(34 + input_length + 1, 10)
                    elif input_length <= 8:
                        core.goto_xy(34 + input_length + 2, 10)
            elif key == 27:
                record_outcome_select_date(username, amount, category, wallet_id)
                status = 0
                break

        if key == 13:
            day = int(date[:2])
            month = int(date[2:4])
            year = int(date[4:])
            status = core.check_date(day, month, year)
            if status == 0:
                record_outcome_time(username, amount, category, wallet_id, date)
                break
            else:
                date = "0"
                menu.show_message("Tanggal tidak valid", 13, status)
                core.get_key()


def record_outcome_time(username, amount, category, wallet_id, date):
    input_length = 0
    status = 1
    time = "0"

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran (Tentukan Waktu - 24 Jam)")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Kategori Pengeluaran\t\t: \033[92m{category}\033[0m")
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{wallet.get_wallet_name(username, wallet_id)}\033[0m")
    menu.text_menu(f"Tanggal \t\t\t: \033[92m{core.format_date_2(date)}\033[0m")
    while status == 1:
        core.goto_xy(0, 11)
        menu.text_menu(f"Waktu \t\t\t: {core.format_time(int(time))}")
        time = ""
        menu.text_menu("Keterangan (Opsional)\t: ")
        menu.back_instruction()
        core.goto_xy(34, 11)

        while True:
            key = ord(core.get_key())

            if core.check_key(key, True) and (input_length < 4):
                time += chr(key)
                print(f"\033[92m{chr(key)}\033[0m")
                input_length += 1
                core.goto_xy(34, 11)
                print("                     ")
                core.goto_xy(34, 11)
                print(f"\033[92m{core.format_time(int(time))}\033[0m")
                if input_length < 2:
                    core.goto_xy(34 + input_length, 11)
                elif input_length <= 4:
                    core.goto_xy(34 + input_length + 1, 11)
            elif key == 13:
                if input_length == 4:
                    input_length = 0
                    break
            elif key == 8:
                if input_length > 0:
                    input_length -= 1
                    time = time[:-1]
                    core.goto_xy(34, 11)
                    print("                     ")
                    core.goto_xy(34, 11)
                    if time == "":
                        print(f"\033[92m{core.format_time(0)}\033[0m")
                    else:
                        print(f"\033[92m{core.format_time(int(time))}\033[0m")
                    if input_length < 2:
                        core.goto_xy(34 + input_length, 11)
                    elif input_length <= 4:
                        core.goto_xy(34 + input_length + 1, 11)
            elif key == 27:
                record_outcome_select_date(username, amount, category, wallet_id)
                status = 0
                break

        if key == 13:
            hour = time[:2]
            minute = time[2:]
            status = core.check_time(hour, minute)
            if status == 0:
                record_outcome_note(username, amount, category, wallet_id, date, time)
                break
            else:
                time = "0"
                menu.show_message("Waktu tidak valid", 13, status)
                core.get_key()


def record_outcome_note(username, amount, category, wallet_id, date, time):
    input_length = 0
    note = ""

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran (Tambahkan Keterangan)")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Kategori Pengeluaran\t\t: \033[92m{category}\033[0m")
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{wallet.get_wallet_name(username, wallet_id)}\033[0m")
    menu.text_menu(f"Tanggal \t\t\t: \033[92m{core.format_date_2(date)}\033[0m")
    menu.text_menu(f"Waktu \t\t\t: \033[92m{core.format_time(time)}\033[0m")
    menu.text_menu("Keterangan (Opsional)\t: ")
    menu.back_instruction()
    core.goto_xy(34, 12)

    while True:
        key = ord(core.get_key())

        if core.check_key(key) and (input_length < 20):
            note += chr(key)
            print(f"\033[92m{chr(key)}\033[0m")
            input_length += 1
            core.goto_xy(34 + input_length, 12)
        elif key == 13:
            break
        elif key == 8:
            if input_length > 0:
                print("\b \b")
                input_length -= 1
                note = note[:-1]
                core.goto_xy(34 + input_length, 12)
        elif key == 27:
            record_outcome_time(username, amount, category, wallet_id, date)
            break

    if key == 13:
        record_outcome_confirm(username, amount, category, wallet_id, date, time, note)
        pass


def record_outcome_confirm(username, amount, category, wallet_id, date, time, note):
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Catat Pengeluaran")
    menu.h_line()
    menu.text_menu(f"Jumlah Pengeluaran\t\t: \033[92m{core.format_rupiah(int(amount))}\033[0m")
    menu.text_menu(f"Kategori Pengeluaran\t\t: \033[92m{category}\033[0m")
    menu.text_menu(f"Dompet Asal\t\t\t: \033[92m{wallet.get_wallet_name(username, wallet_id)}\033[0m")
    menu.text_menu(f"Tanggal \t\t\t: \033[92m{core.format_date_2(date)}\033[0m")
    menu.text_menu(f"Waktu \t\t\t: \033[92m{core.format_time(time)}\033[0m")
    menu.text_menu(f"Keterangan (Opsional)\t: \033[92m{note}\033[0m")
    menu.h_line()
    menu.text_menu("Konfirmasi Pengeluaran")
    balance = wallet.get_wallet_balance(username, wallet_id)
    menu.text_menu(f"\033[95m{wallet.get_wallet_name(username, wallet_id)}\033[0m : \033[94m{core.format_rupiah(balance)}\033[0m →  \033[94m{core.format_rupiah(balance - int(amount))}\033[0m")
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
                status = activity.add_record(username, amount, category, wallet_id, date, time, note, "Pengeluaran")
                if status == 0:
                    menu.show_message("Berhasil mencatat pengeluaran", 19, status)
                    core.get_key()
                    menu.home_menu(username)
                    break
                else:
                    menu.show_message("Saldo dompet kurang", 19, status)
                    core.get_key()
            elif current_selection == 2:
                record_outcome_note(username, amount, category, wallet_id, date, time)
                break

