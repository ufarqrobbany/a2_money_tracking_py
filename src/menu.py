from src import core
from src import account


def h_line():
    print(" ════════════════════════════════════════════════════════")


def back_instruction():
    h_line()
    print("   Tekan ESC untuk kembali")
    h_line()


def nav_instruction():
    h_line()
    print("   Gunakan tombol panah untuk navigasi dan tekan Enter")
    h_line()


def show_message(text, y, status=-1):
    core.goto_xy(0, y)
    clear_message()
    core.goto_xy(0, y)
    message(text, status)


def message(text, status):
    h_line()
    color = "\033[1;32m" if status == 0 else "\033[1;31m" if status == 1 else ""
    reset_color = "\033[0m" if color else ""
    print(f"   {color}{text}{reset_color}")
    h_line()


def clear_message():
    h_line()
    print("                                                        ")
    h_line()


def header_menu():
    h_line()
    print("                  \033[1mMONEY TRACKING APP - A2\033[0m ")
    h_line()


def text_menu(text):
    print(f"   {text}")


def option(text, select, index, warning=False):
    marker = "■" if select == index else " "
    color = "\033[1;31m" if warning and marker == "■" else "\033[1;32m" if not warning else ""
    reset_color = "\033[0m" if color else ""
    print(f"   [{color}{marker}{reset_color}] {text}")


def first_menu():
    current_selection = 1

    core.clear_screen()
    header_menu()
    text_menu("Selamat Datang di Aplikasi Money Tracking")
    text_menu("Catat dan kelola keuanganmu dengan mudah")
    h_line()
    core.goto_xy(0, 9)
    nav_instruction()
    while True:
        core.goto_xy(0, 6)
        option("Masuk", current_selection, 1)
        option("Daftar", current_selection, 2)
        option("Keluar", current_selection, 3, True)
        core.goto_xy(0, 0)

        key = ord(core.get_key())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 3:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                account.login_menu()
            elif current_selection == 2:
                account.register_menu()
            break


# def home_menu(username):
