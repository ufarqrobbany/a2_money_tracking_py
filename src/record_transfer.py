from src import core
from src import menu
from src import account
import datetime

def record_transfer_source_wallet(username):
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
    now = datetime.datetime.now().date().strftime('%d%m%Y')
    menu.text_menu(f"Tanggal \t\t\t: {core.format_date_2(now)}")
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
                        record_outcome_select_date(username, amount, category, wallet_id)
                    elif current_selection == total_wallet + 1:
                        record_outcome_select_category(username, amount)
                    break