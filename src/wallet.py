import menu
import core

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
                    tampil_menu_tambah_dompet(username)
                else:
                    core.gotoxy(1, 12 + jml_dompet)
                    print("Tidak bisa menambah dompet, maksimal 10 dompet dalam 1 akun")
                    core.get_key()
            elif current_selection == 2:
                tampil_menu_ubah_nama_dompet(username)
            elif current_selection == 3:
                if jml_dompet > 1:
                    tampil_menu_hapus_dompet(username)
                else:
                    core.gotoxy(1, 12 + jml_dompet)
                    print("Tidak bisa menghapus dompet lagi, sisakan 1 dompet di akunmu")
                    core.get_key()
            elif current_selection == 4:
                menu.home_menu(username)
            break

def tampil_menu_tambah_dompet(username):
    nama_dompet = ""
    saldo_awal = ""
    key = ''
    jml_dompet = 0
    n = 0
    p = 1
    status = 1
    saldo = 0

    while status == 1:
        core.clear_screen()

        # Print header
        menu.header_menu()
        menu.text_menu("Nama :")
        menu.h_line()
        menu.text_menu("Tambah dompet baru")
        menu.h_line()

        #jml_dompet = get_dompet(username, True)

        menu.h_line()
        menu.text_menu("Nama Dompet\t: ")
        menu.text_menu("Saldo Awal\t: ", end='')
        #format_rupiah(saldo)
        menu.back_instruction()
        core.goto_xy(19, 4 + jml_dompet + 5)

        while True:
            key = ord(core.get_key())
            if (key.isalnum() or key.isdigit() or key == ' ' or (n<20)):
                if (p == 1):
                    nama_dompet = key
                    n += 1
                    print(key)
                    core.goto_xy(19 + n, 8 + p + jml_dompet)
                elif ((p == 2) and (key >= '0' and key <= '9') and (n < 8)):
                    saldo_awal[n] = key
                    n += 1
                    saldo = int(''.join(saldoawal))
                    core.goto_xy(19, 8 + p + jml_dompet)
                    print("                  ", end='')
                    core.goto_xy(19, 8 + p + jml_dompet)
                    #format_rupiah(saldo)
                    #core.goto_xy(19 + get_length_format_rupiah(saldo) + 2, 8 + p + jml_dompet)
            elif key == 13:
                if n == 0 and p == 2:
                    saldo = 0
                    p = 1
                    n = 0
                    break
                if n > 0:
                    if p == 1:
                        nama_dompet[n] = '\0'
                        p = 2
                        n = 0
                        core.goto_xy(19 + n + 2, 8 + p + jml_dompet)
                    else:
                        saldoawal[n] = '\0'
                        saldo = int(''.join(saldoawal))
                        p = 1
                        n = 0
                        break
            elif key == 8:
                if n > 0:
                    if p == 1:
                        print("\b \b", end='', flush=True)
                    n -= 1
                    if p == 2:
                        saldoawal[n] = '\0'
                        saldo = int(''.join(saldoawal)) if saldoawal[0] else 0
                        core.goto_xy(19, 5 + p + jml_dompet)
                        print("                  ", end='')
                        core.goto_xy(19, 5 + p + jml_dompet)
                        #format_rupiah(saldo)
                        #core.goto_xy(19 + get_length_format_rupiah(saldo) + 2, 5 + p + jml_dompet)
            elif key == 27:
                break
            
        if key == 13:
            core.goto_xy(1, 9 + 2 + jml_dompet)
            #status = tambah_dompet(username, nama_dompet, saldo)
            input()

            if status == 1:
                saldoawal = [' '] * 9
                saldo = 0

                core.goto_xy(19, 5 + p + jml_dompet)
                print("                  ", end='')
                core.goto_xy(19, 5 + p + jml_dompet)
                #format_rupiah(saldo)
                #core.goto_xy(19 + get_length_format_rupiah(saldo) + 2, 5 + p + jml_dompet)

        if key == 27 or status == 0:
            break

    if status == 0:
        print()
        #tampil_menu_dompet(username)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes

def get_last_dompet(username):
    file_name = f"data/data.json"
    id_dompet = 0

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            for user in data:
                if user['username'] == username:
                    for wallet in user['wallet']:
                        id_dompet = wallet['id']
        return id_dompet
    except FileNotFoundError:
        print(f"\nGagal membuka file dompet {file_name}\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")
>>>>>>> Stashed changes
