from src import core
from src import menu
from src import account
from src.wallet import get_wallet_name, get_total_balance
import datetime


def get_total_income_month(username):
    data = core.read_data()
    total_income = 0
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    if activity["type"] == "Pemasukan":
                        total_income += int(activity["amount"])
    return total_income


def get_total_outcome_month(username):
    data = core.read_data()
    total_income = 0
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    if activity["type"] == "Pengeluaran":
                        total_income += int(activity["amount"])
    return total_income


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


def monthly_recap_select_year(username):
    core.goto_xy(0, 0)
    current_selection = 1
    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Bulanan (Pilih Tahun)")
    menu.h_line()

    list_years = []

    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    tahun = activity["datetime"].split()[0]
                    list_years.append(tahun[4:])

    list_years = sorted(set(list_years), reverse=True)

    core.goto_xy(0, 8 + len(list_years))
    menu.nav_instruction()

    while True:
        core.goto_xy(0, 7)
        for index, year in enumerate(list_years):
            menu.option(
                f"Tahun {year}", current_selection, index + 1)
        menu.option("Kembali", current_selection, len(list_years) + 1, True)
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < len(list_years) + 1:
            current_selection += 1
        elif key == 13:
            if current_selection <= len(list_years):
                monthly_recap_select_month(username, list_years[current_selection - 1])
            elif current_selection == len(list_years) + 1:
                monthly_recap_menu(username)
            break


def annual_recap(username, year):
    core.goto_xy(0, 0)
    data = core.read_data()
    total_outcome = 0
    total_income = 0
    income_categories = {}
    outcome_categories = {}

    core.clear_screen()
    all_activities = []

    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    activity_year = datetime.datetime.strptime(activity['datetime'], '%d%m%Y %H%M').strftime('%Y')
                    if activity_year == year:
                        all_activities.append(activity)
                        if activity["type"] == "Pemasukan":
                            total_income += int(activity["amount"])
                            income_categories[activity["category"]] = income_categories.get(activity["category"], 0) + int(activity["amount"])
                        elif activity["type"] == "Pengeluaran":
                            total_outcome += int(activity["amount"])
                            outcome_categories[activity["category"]] = outcome_categories.get(activity["category"], 0) + int(activity["amount"])

    sorted_all_activities = sorted(all_activities,
                                   key=lambda x: datetime.datetime.strptime(x['datetime'], '%d%m%Y %H%M'),
                                   reverse=True)

    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu(f"Rekap Tahun {year}")
    menu.h_line()
    menu.text_menu(f"Total Pemasukan\t: \033[94m{core.format_rupiah(total_income)}\033[0m")
    menu.text_menu(f"Total Pengeluaran\t: \033[94m{core.format_rupiah(total_outcome)}\033[0m")

    menu.h_line()
    menu.text_menu("Persentase Pemasukan per Kategori:")
    for category, amount in income_categories.items():
        percentage = (amount / total_income) * 100
        menu.text_menu(
            f"   {category}: \033[95m{percentage:.2f}%\033[0m (Total: \033[94m{core.format_rupiah(amount)}\033[0m)")
    if len(income_categories) == 0:
        menu.text_menu("   Tidak ada kategori")

    print("")
    menu.text_menu("Persentase Pengeluaran per Kategori:")
    for category, amount in outcome_categories.items():
        percentage = (amount / total_outcome) * 100
        menu.text_menu(
            f"   {category}: \033[95m{percentage:.2f}%\033[0m (Total: \033[94m{core.format_rupiah(amount)}\033[0m)")
    if len(outcome_categories) == 0:
        menu.text_menu("   Tidak ada kategori")

    menu.h_line()
    for index, activity in enumerate(sorted_all_activities):
        menu.text_menu(f"Tanggal\t\t: {core.format_date_2(activity['datetime'].split()[0])}")
        menu.text_menu(f"Waktu\t\t: {core.format_time(activity['datetime'].split()[1])}")
        if activity["type"] == "Pengeluaran":
            menu.text_menu(f"Jenis\t\t: \033[31m{activity['type']}\033[0m")
            menu.text_menu(f"Kategori\t\t: {activity['category']}")
            menu.text_menu(f"Nominal\t\t: \033[94m{core.format_rupiah(int(activity['amount']))}\033[0m")
            menu.text_menu(f"Dompet Asal\t\t: \033[95m{get_wallet_name(username, activity['wallet_id'])}\033[0m")
        elif activity["type"] == "Pemasukan":
            menu.text_menu(f"Jenis\t\t: \033[92m{activity['type']}\033[0m")
            menu.text_menu(f"Kategori\t\t: {activity['category']}")
            menu.text_menu(f"Nominal\t\t: \033[94m{core.format_rupiah(int(activity['amount']))}\033[0m")
            menu.text_menu(f"Dompet Tujuan\t: \033[95m{get_wallet_name(username, activity['wallet_id'])}\033[0m")
        elif activity["type"] == "Transfer":
            menu.text_menu(f"Jenis\t\t: \033[33m{activity['type']}\033[0m")
            menu.text_menu(f"Nominal\t\t: \033[94m{core.format_rupiah(int(activity['amount']))}\033[0m")
            menu.text_menu(f"Dompet Asal\t\t: \033[95m{get_wallet_name(username, activity['source_wallet_id'])}\033[0m")
            menu.text_menu(f"Dompet Tujuan\t: \033[95m{get_wallet_name(username, activity['destination_wallet_id'])}\033[0m")
        menu.text_menu(f"Keterangan\t\t: {activity['note']}")

        if index < len(sorted_all_activities) - 1:
            menu.text_menu(f"----------------------------------------------------")

    print("")

    menu.h_line()
    menu.text_menu("Tekan ESC untuk kembali")
    menu.h_line()

    while True:
        key = ord(core.get_key())

        if key == 27:
            core.clear_screen()
            recap_menu(username)
            break


def category_recap(username):
    core.goto_xy(0, 0)
    data = core.read_data()
    income_categories = {}
    outcome_categories = {}
    total_income = 0
    total_outcome = 0

    core.clear_screen()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    if activity["type"] == "Pemasukan":
                        income_categories[activity["category"]] = income_categories.get(activity["category"],
                                                                                        0) + int(activity["amount"])
                        total_income += int(activity["amount"])
                    elif activity["type"] == "Pengeluaran":
                        outcome_categories[activity["category"]] = outcome_categories.get(activity["category"],
                                                                                          0) + int(
                            activity["amount"])
                        total_outcome += int(activity["amount"])

    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Kategori")
    menu.h_line()
    menu.text_menu(f"Total Pemasukan: \033[94m{core.format_rupiah(total_income)}\033[0m")
    menu.text_menu(f"Total Pengeluaran: \033[94m{core.format_rupiah(total_outcome)}\033[0m")

    sorted_income_categories = sorted(income_categories.items(), key=lambda x: x[1], reverse=True)
    sorted_outcome_categories = sorted(outcome_categories.items(), key=lambda x: x[1], reverse=True)

    print("")
    menu.text_menu("Persentase Pemasukan per Kategori:")
    for in_category, in_amount in sorted_income_categories:
        percentage = (in_amount / total_income) * 100
        menu.text_menu(f"   {in_category}: \033[95m{percentage:.2f}%\033[0m (Total: \033[94m{core.format_rupiah(in_amount)}\033[0m)")

    print("")
    menu.text_menu("Persentase Pengeluaran per Kategori:")
    for out_category, out_amount in sorted_outcome_categories:
        percentage = (out_amount / total_outcome) * 100
        menu.text_menu(f"   {out_category}: \033[95m{percentage:.2f}%\033[0m (Total: \033[94m{core.format_rupiah(out_amount)}\033[0m)")

    menu.h_line()
    menu.text_menu("Tekan ESC untuk kembali")
    menu.h_line()

    while True:
        key = ord(core.get_key())

        if key == 27:
            recap_menu(username)
            break

            
def all_income(username):
    core.goto_xy(0, 0)
    data = core.read_data()
    total_income = 0

    core.clear_screen()
    income_activities = []

    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    if activity["type"] == "Pemasukan":
                        total_income += int(activity["amount"])
                        income_activities.append(activity)

    sorted_income_activities = sorted(income_activities, key=lambda x: datetime.datetime.strptime(x['datetime'], '%d%m%Y %H%M'), reverse=True)

    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Semua Pemasukan")
    menu.h_line()
    menu.text_menu(f"Total Pemasukan: \033[94m{core.format_rupiah(total_income)}\033[0m")

    print("")
    for index, activity in enumerate(sorted_income_activities):
        menu.text_menu(f"Tanggal\t\t: {core.format_date_2(activity['datetime'].split()[0])}")
        menu.text_menu(f"Waktu\t\t: {core.format_time(activity['datetime'].split()[1])}")
        menu.text_menu(f"Kategori\t\t: {activity['category']}")
        menu.text_menu(f"Nominal\t\t: \033[94m{core.format_rupiah(int(activity['amount']))}\033[0m")
        menu.text_menu(f"Dompet Tujuan\t: \033[95m{get_wallet_name(username, activity['wallet_id'])}\033[0m")
        menu.text_menu(f"Keterangan\t\t: {activity['note']}")

        if index < len(sorted_income_activities) - 1:
            menu.text_menu(f"----------------------------------------------------")

    print("")
    menu.h_line()
    menu.text_menu("Tekan ESC untuk kembali")
    menu.h_line()

    while True:
        key = ord(core.get_key())

        if key == 27:
            core.clear_screen()
            recap_menu(username)
            break


def all_outcome(username):
    core.goto_xy(0, 0)
    data = core.read_data()
    total_outcome = 0

    core.clear_screen()
    outcome_activities = []

    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    if activity["type"] == "Pengeluaran":
                        total_outcome += int(activity["amount"])
                        outcome_activities.append(activity)

    sorted_outcome_activities = sorted(outcome_activities,
                                      key=lambda x: datetime.datetime.strptime(x['datetime'], '%d%m%Y %H%M'),
                                      reverse=True)

    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Semua Pengeluaran")
    menu.h_line()
    menu.text_menu(f"Total Pengeluaran: \033[94m{core.format_rupiah(total_outcome)}\033[0m")

    print("")
    for index, activity in enumerate(sorted_outcome_activities):
        menu.text_menu(f"Tanggal\t\t: {core.format_date_2(activity['datetime'].split()[0])}")
        menu.text_menu(f"Waktu\t\t: {core.format_time(activity['datetime'].split()[1])}")
        menu.text_menu(f"Kategori\t\t: {activity['category']}")
        menu.text_menu(f"Nominal\t\t: \033[94m{core.format_rupiah(int(activity['amount']))}\033[0m")
        menu.text_menu(f"Dompet Asal\t\t: \033[95m{get_wallet_name(username, activity['wallet_id'])}\033[0m")
        menu.text_menu(f"Keterangan\t\t: {activity['note']}")

        if index < len(sorted_outcome_activities) - 1:
            menu.text_menu(f"----------------------------------------------------")

    print("")
    menu.h_line()
    menu.text_menu("Tekan ESC untuk kembali")
    menu.h_line()

    while True:
        key = ord(core.get_key())

        if key == 27:
            core.clear_screen()
            recap_menu(username)
            break

def monthly_recap_menu(username):
    core.goto_xy(0, 0)
    current_selection = 1

    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Bulanan")
    menu.h_line()
    core.goto_xy(0, 11)
    menu.nav_instruction()

    today = datetime.date.today()
    this_month = (datetime.date(today.year, today.month, 1))
    last_month = (this_month - datetime.timedelta(days=this_month.day))

    while True:
        core.goto_xy(0, 7)
        menu.option(
            f"Bulan Ini ({core.format_date_2(this_month.strftime("%d%m%Y"), False)})",
            current_selection, 1)
        menu.option(
            f"Bulan Kemarin ({core.format_date_2(last_month.strftime("%d%m%Y"), False)})",
            current_selection, 2)
        menu.option("Pilih Bulan", current_selection, 3)
        menu.option("Kembali", current_selection, 4, True)
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 4:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                monthly_recap(username, this_month.strftime("%m%Y"))
            elif current_selection == 2:
                monthly_recap(username, last_month.strftime("%m%Y"))
            elif current_selection == 3:
                monthly_recap_select_year(username)
            elif current_selection == 4:
                recap_menu(username)
            break


def annual_recap_menu(username):
    core.goto_xy(0, 0)
    current_selection = 1
    core.clear_screen()
    menu.header_menu()
    menu.text_menu(f"Nama : \033[95m{account.get_account_name(username)}\033[0m")
    menu.h_line()
    menu.text_menu("Rekap Tahunan")
    menu.h_line()

    list_years = []

    data = core.read_data()
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    tahun = activity["datetime"].split()[0]
                    list_years.append(tahun[4:])

    list_years = sorted(set(list_years), reverse=True)

    core.goto_xy(0, 8 + len(list_years))
    menu.nav_instruction()

    while True:
        core.goto_xy(0, 7)
        for index, year in enumerate(list_years):
            menu.option(
                f"Tahun {year}", current_selection, index + 1)
        menu.option("Kembali", current_selection, len(list_years) + 1, True)
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < len(list_years) + 1:
            current_selection += 1
        elif key == 13:
            if current_selection <= len(list_years):
                annual_recap(username, list_years[current_selection - 1])
            elif current_selection == len(list_years) + 1:
                recap_menu(username)
            break
