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
                    # tampil_menu_tambah_dompet(username)
                else:
                    core.gotoxy(1, 12 + jml_dompet)
                    print("Tidak bisa menambah dompet, maksimal 10 dompet dalam 1 akun")
                    core.get_key()
            elif current_selection == 2:
                # tampil_menu_ubah_nama_dompet(username)
            elif current_selection == 3:
                if jml_dompet > 1:
                    # tampil_menu_hapus_dompet(username)
                else:
                    core.gotoxy(1, 12 + jml_dompet)
                    print("Tidak bisa menghapus dompet lagi, sisakan 1 dompet di akunmu")
                    core.get_key()
            elif current_selection == 4:
                menu.home_menu(username)
            break

def newDompet(nama_dompet, saldo_awal):
    dataBaru = {
        "id": 1,
        "nama_dompet": nama_dompet,
        "saldo": saldo_awal,
        "actitivy": []
    }
    return [dataBaru]

def tambahDompet(username, nama_dompet, saldo_awal):
    data = core.read_data()
    found = False
    index = None
    for i in range(len(data)):
        if data[i]['username'] == username:
            found = True
            index = i
            break
    if found:
        data[index]['wallet'].append(newDompet(nama_dompet, saldo_awal))
        core.write_data(data)
        return 0
    else:
        return 1