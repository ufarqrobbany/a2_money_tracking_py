from src import core
import msvcrt

if __name__ == '__main__':
    current_selection = 3

    while True:
        core.clear_screen()
        print(" ════════════════════════════════════════════════════════")
        print("                  \033[1mMONEY TRACKING APP - A2\033[0m ")
        print(" ════════════════════════════════════════════════════════")
        print("   Selamat Datang di Aplikasi Money Tracking")
        print("   Catat dan kelola keuanganmu dengan mudah")
        print(" ════════════════════════════════════════════════════════")
        print("   [" + ("■" if current_selection == 1 else " ") + "] Masuk")
        print("   [" + ("■" if current_selection == 2 else " ") + "] Daftar")
        print("   [\033[1;31m" + ("■" if current_selection == 3 else " ") + "\033[0m] Keluar")
        print(" ════════════════════════════════════════════════════════")
        print("   Gunakan tombol panah untuk navigasi dan tekan Enter")

        key = ord(msvcrt.getch())

        if key == 72 and current_selection > 1:
            current_selection -= 1
        elif key == 80 and current_selection < 3:
            current_selection += 1
        elif key == 13:
            if current_selection == 1:
                print("Login")
            elif current_selection == 2:
                print("Register")
            break
