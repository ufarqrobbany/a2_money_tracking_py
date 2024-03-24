from src import core
from src import menu
from src import account
from src.wallet import get_wallet_name, get_total_balance
import datetime


def recap_menu(username, refresh=True):
    core.goto_xy(0, 0)
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu(
        f"Total Saldo saat ini (Semua Dompet)\t: \033[94m{core.format_rupiah(get_total_balance(username))}\033[0m")
    menu.text_menu(
        f"Pemasukan Bulan Ini ({core.get_date(False, False)})\t: \033[94m{core.format_rupiah(get_total_income_month(username))}\033[0m")
    menu.text_menu(
        f"Pengeluaran Bulan Ini ({core.get_date(False, False)})\t: \033[94m{core.format_rupiah(get_total_outcome_month(username))}\033[0m")
    menu.h_line()
    menu.text_menu("Lihat Rekap")
    menu.h_line()
    core.goto_xy(0, 19)
    menu.nav_instruction()

    if refresh:
        recap_menu(username, False)
    else:
        while True:
            core.goto_xy(0, 11)
            menu.option("Rekap Harian", current_selection, 1)
            menu.option("Rekap Mingguan", current_selection, 2)
            menu.option("Rekap Bulanan", current_selection, 3)
            menu.option("Rekap Tahunan", current_selection, 4)
            menu.option("Rekap Kategori", current_selection, 5)
            menu.option("Rekap Semua Pemasukan", current_selection, 6)
            menu.option("Rekap Semua Pengeluaran", current_selection, 7)
            menu.option("Kembali", current_selection, 8, True)
            core.goto_xy(0, 0)

            key = ord(core.get_key())

            if key == 72 and current_selection > 1:
                current_selection -= 1
            elif key == 80 and current_selection < 8:
                current_selection += 1
            elif key == 13:
                if current_selection == 1:
                    daily_recap_menu(username)
                elif current_selection == 2:
                    weekly_recap_menu(username)
                elif current_selection == 3:
                    monthly_recap_menu(username)
                elif current_selection == 4:
                    annual_recap_menu(username)
                elif current_selection == 5:
                    category_recap(username)
                elif current_selection == 6:
                    all_income(username)
                elif current_selection == 7:
                    all_outcome(username)
                elif current_selection == 8:
                    menu.home_menu(username)
                break


def daily_recap_menu(username):
    core.goto_xy(0, 0)
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Harian")
    menu.h_line()
    core.goto_xy(0, 11)
    menu.nav_instruction()

    today = datetime.date.today()
    yesterday = (today - datetime.timedelta(days=1))

    while True:
        core.goto_xy(0, 7)
        menu.option(f"Hari Ini ({core.format_date_2(today.strftime("%d%m%Y"))})", current_selection, 1)
        menu.option(f"Kemarin ({core.format_date_2(yesterday.strftime("%d%m%Y"))})", current_selection, 2)
        menu.option("Pilih Tanggal", current_selection, 3)
        menu.option("Kembali", current_selection, 4, True)
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 4:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                daily_recap(username, today.strftime("%d%m%Y"))
            elif current_selection == 2:
                daily_recap(username, yesterday.strftime("%d%m%Y"))
            elif current_selection == 3:
                daily_recap_input(username)
            elif current_selection == 4:
                recap_menu(username)
            break


def daily_recap_input(username):
    input_length = 0
    date = "0"
    status = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Harian (Pilih Tanggal)")
    menu.h_line()
    while status == 1:
        core.goto_xy(0, 7)
        menu.text_menu(f"Tanggal \t: {core.format_date(date)}")
        date = ""
        menu.back_instruction()
        core.goto_xy(18, 7)

        while True:
            key = ord(core.get_key())

            if core.check_key(key, True) and (input_length < 8):
                date += chr(key)
                print(f"\033[92m{chr(key)}\033[0m")
                input_length += 1
                core.goto_xy(18, 7)
                print("                     ")
                core.goto_xy(18, 7)
                print(f"\033[92m{core.format_date(date)}\033[0m")
                if input_length < 2:
                    core.goto_xy(18 + input_length, 7)
                elif input_length < 4:
                    core.goto_xy(18 + input_length + 1, 7)
                elif input_length <= 8:
                    core.goto_xy(18 + input_length + 2, 7)
            elif key == 13:
                if input_length == 8:
                    input_length = 0
                    break
            elif key == 8:
                if input_length > 0:
                    input_length -= 1
                    date = date[:-1]
                    core.goto_xy(18, 7)
                    print("                     ")
                    core.goto_xy(18, 7)
                    if date == "":
                        print(f"\033[92m{core.format_date(0)}\033[0m")
                    else:
                        print(f"\033[92m{core.format_date(date)}\033[0m")
                    if input_length < 2:
                        core.goto_xy(18 + input_length, 7)
                    elif input_length < 4:
                        core.goto_xy(18 + input_length + 1, 7)
                    elif input_length <= 8:
                        core.goto_xy(18 + input_length + 2, 7)
            elif key == 27:
                daily_recap_menu(username)
                status = 0
                break

        if key == 13:
            day = int(date[:2])
            month = int(date[2:4])
            year = int(date[4:])
            status = core.check_date(day, month, year)
            if status == 0:
                daily_recap(username, date)
                break
            else:
                date = "0"
                menu.show_message("Tanggal tidak valid", 8, status)
                core.get_key()


def weekly_recap_menu(username):
    core.goto_xy(0, 0)
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Mingguan")
    menu.h_line()
    core.goto_xy(0, 10)
    menu.nav_instruction()

    today = datetime.date.today()
    days_to_sunday = (6 - today.weekday()) % 7
    next_sunday = today + datetime.timedelta(days=days_to_sunday)

    while True:
        core.goto_xy(0, 7)
        week_start = next_sunday - datetime.timedelta(days=7 * 0)
        week_end = week_start + datetime.timedelta(days=6)
        menu.option(
            f"Minggu Ini ({core.format_date_2(week_start.strftime("%d%m%Y"))} - {core.format_date_2(week_end.strftime("%d%m%Y"))})",
            current_selection, 1)
        week_start_2 = next_sunday - datetime.timedelta(days=7 * 1)
        week_end_2 = week_start_2 + datetime.timedelta(days=6)
        menu.option(
            f"Minggu Lalu ({core.format_date_2(week_start_2.strftime("%d%m%Y"))} - {core.format_date_2(week_end_2.strftime("%d%m%Y"))})",
            current_selection, 2)
        menu.option("Kembali", current_selection, 3, True)
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 3:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                weekly_recap(username, week_start, week_end)
            elif current_selection == 2:
                weekly_recap(username, week_start_2, week_end_2)
            elif current_selection == 3:
                recap_menu(username)
            break

