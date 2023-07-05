import datetime


def main():
    print("Selamat datang di Kantin ITTP!")
    print("1. Login")
    print("2. Register")

    choice = input("Pilihan: ")
    if choice == "1":
        user_data = login()
        show_home(user_data)
    elif choice == "2":
        register()
        main()
    else:
        print("Pilihan tidak valid.")
        main()


def login():
    while True:
        username = input("Username: ")
        password = input("Password: ")
        with open("user.txt", "r") as file:
            users = file.readlines()
            for user in users:
                user_data = user.strip().split(",")
                if username == user_data[4]:
                    if password == user_data[5]:
                        return user_data
                    else:
                        print("Password salah. Silakan coba lagi.")
                        break
            else:
                choice = input("Tampaknya anda belum memiliki akun, register sekarang? (y/n) ")
                if choice.lower() == "y":
                    register()
                else:
                    print("Terima kasih. Sampai jumpa!")
                    exit()


def register():
    while True:
        nama_lengkap = input("Nama Lengkap: ")
        nim = input("NIM: ")
        prodi = input("Prodi: ")
        username = input("Username: ")
        password = input("Password: ")

        if not all([nama_lengkap, nim, prodi, username, password]):
            print("Semua field harus diisi. Silakan coba kembali.")
            continue

        with open("user.txt", "r") as file:
            users = file.readlines()

        for user in users:
            data = user.strip().split(",")
            if data[2] == nim or data[4] == username:
                print("'{}' tersebut telah terpakai, silahkan coba kembali."
                      .format(nim if data[2] == nim else username))
                break

        else:
            if len(users) > 0:
                last_user = users[-1].strip().split(",")
                id_user = str(int(last_user[0]) + 1)
            else:
                id_user = "0"

            with open("user.txt", "a") as file:
                file.write(f"{id_user},{nama_lengkap},{nim},{prodi},{username},{password}\n")

            print("Registrasi berhasil, akun anda telah terbuat. Silahkan login")
            break


def show_home(user_data):
    nama_lengkap = user_data[1]
    print(f"\nHallo {nama_lengkap}! Selamat datang di Kantin ITTP!")
    print("Mana kantin pilihanmu?")

    kantins = set()
    with open("kantin.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            kantins.add(data[1])

    if len(kantins) > 1:
        print("Pilihan Kantin:")
        for i, kantin in enumerate(kantins, start=1):
            print(f"{i}. {kantin}")
        print(f"{len(kantins) + 1}. Cari nama menu")
        print(f"{len(kantins) + 2}. Lainnya")

        while True:
            choice = input("Pilihan: ")

            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(kantins):
                    selected_kantin = list(kantins)[choice - 1]
                    show_kantin(user_data, selected_kantin)
                    return
                elif choice == len(kantins) + 1:
                    search_menu(user_data)
                    return
                elif choice == len(kantins) + 2:
                    show_lainnya(user_data)
                    return
            print("Inputan tidak valid, masukkan ulang pilihanmu:")

    print("Pilihan tidak valid.")
    show_home(user_data)  # Memanggil kembali fungsi show_home jika pilihan tidak valid


def search_menu(user_data):
    search_keyword = input("Masukkan kata kunci untuk mencari nama menu: ")

    search_results = []
    with open("kantin.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            menu_name = data[4]
            if search_keyword.lower() in menu_name.lower():
                search_results.append(data)

    if search_results:
        print(f"\nBerikut hasil dari '{search_keyword}':")
        for i, result in enumerate(search_results, start=1):
            print(f"\n{i}. Nama Menu: {result[4]}")
            print(f"Harga: {result[5]}")
            print(f"Nama Warung: {result[2]}")
            print(f"Lokasi Kantin: {result[1]}")

        print(f"\nTerdapat {len(search_results)} data dari pencarianmu.")
        print("1. Urutkan data dari harga termurah")
        print("2. Urutkan data dari harga termahal")
        print("3. Kembali ke halaman home")

        choice = input("Pilihan: ")
        if choice == "1":
            sorted_results = sorted(search_results, key=lambda x: int(x[5]))
            print(f"\nBerikut harga termurah ke yang termahal dari pencarian '{search_keyword}':")
            for i, result in enumerate(sorted_results, start=1):
                print(f"\n{i}. Nama Menu: {result[4]}")
                print(f"Harga: {result[5]}")
                print(f"Nama Warung: {result[2]}")
                print(f"Lokasi Kantin: {result[1]}")

            input("\nTekan enter untuk kembali ke halaman home.")
            show_home(user_data)
        elif choice == "2":
            sorted_results = sorted(search_results, key=lambda x: int(x[5]), reverse=True)
            print(f"\nBerikut harga termahal ke yang termurah dari pencarian '{search_keyword}':")
            for i, result in enumerate(sorted_results, start=1):
                print(f"\n{i}. Nama Menu: {result[4]}")
                print(f"Harga: {result[5]}")
                print(f"Nama Warung: {result[2]}")
                print(f"Lokasi Kantin: {result[1]}")

            input("\nTekan enter untuk kembali ke halaman home.")
            show_home(user_data)
        elif choice == "3":
            show_home(user_data)
        else:
            print("Pilihan tidak valid.")
    else:
        print(f"Maaf, '{search_keyword}' tidak ditemukan. Ketik enter untuk kembali ke halaman home.")
        input()
        show_home(user_data)


def show_lainnya(user_data):
    print("\n1. Profil User")
    print("2. Keranjang")
    print("3. Kembali ke halaman Home")
    print("4. Logout")

    choice = input("Pilihan: ")
    if choice == "1":
        show_profil(user_data)
    elif choice == "2":
        show_keranjang(user_data, user_data[4])
    elif choice == "3":
        show_home(user_data)
    elif choice == "4":
        print("Terima kasih telah menggunakan program Kantin ITTP kami!")
        exit()
    else:
        print("Pilihan tidak valid.")
        show_lainnya(user_data)


def show_profil(user_data):
    print("\nProfil user anda sekarang:")
    print(f"Nama Lengkap: {user_data[1]}")
    print(f"NIM: {user_data[2]}")
    print(f"Prodi: {user_data[3]}")
    print(f"Username: {user_data[4]}")
    print(f"Password: {user_data[5]}")

    print("\nTekan enter untuk kembali ke home")
    input()
    show_home(user_data)


def edit_profil(user_data):
    print("\nEdit Profil")
    choice = input("Apakah anda ingin mengedit data anda? Data yang diedit hanya nama lengkap anda! (y/n): ")

    if choice.lower() == "y":
        nama_lengkap = input("Masukkan nama anda: ")

        user_data[1] = nama_lengkap

        with open("user.txt", "r") as file:
            users = file.readlines()

        with open("user.txt", "w") as file:
            for user in users:
                user_info = user.strip().split(",")
                if user_info[0] == user_data[4]:
                    file.write(f"{user_data[0]},{user_data[1]},{user_data[2]},{user_data[3]},"
                               f"{user_data[4]},{user_data[5]}\n")
                else:
                    file.write(user)

        print("Profil berhasil diperbarui.")
        show_home(user_data)
    elif choice.lower() == "n":
        print("Data tidak diubah. Ketik enter untuk kembali ke halaman home.")
        input()
        show_home(user_data)
    else:
        print("Pilihan tidak valid.")
        edit_profil(user_data)


def show_keranjang(user_data, username):
    with open("keranjang.txt", "r") as file:
        keranjang = file.readlines()

    keranjang_found = False
    total_harga = 0
    total_item = 0

    print("\nKeranjang")
    for item in keranjang:
        data = item.strip().split(",")
        if data[1] == username:
            keranjang_found = True
            print(f"Nama Menu: {data[4]}")
            print(f"Nama Warung: {data[3]}")
            print(f"Nama Kantin: {data[2]}")
            print(f"Harga: {data[5]}")
            harga = int(data[5])
            total_harga += harga
            total_item += 1
            print()

    if not keranjang_found:
        print("Keranjang belanja Anda kosong.")
        input("Tekan enter untuk kembali ke halaman home.")
        show_home(user_data)
        return

    print(f"Total menu di keranjang Anda: {total_item}")
    print(f"Total harga: {total_harga}")

    print("\n1. Checkout")
    print("2. Kembali")

    while True:
        choice = input("Pilihan: ")
        if choice == "1":
            checkout(username, total_harga)
            break
        elif choice == "2":
            show_home(user_data)
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan pilihan yang valid.")


def checkout(user_data, username):
    with open("keranjang.txt", "r") as file:
        keranjang = file.readlines()

    if not keranjang:
        print("Keranjang belanja Anda kosong.")
        input("Tekan enter untuk kembali ke halaman home.")
        show_home(user_data)
        return

    with open("histori.txt", "r") as file:
        histori_lines = file.readlines()
        if len(histori_lines) > 0:
            last_histori = histori_lines[-1].strip().split(",")
            histori_id = str(int(last_histori[0]) + 1)
        else:
            histori_id = "0"

    total_harga = 0
    items_to_remove = []

    with open("keranjang.txt", "w") as file:
        for item in keranjang:
            data = item.strip().split(",")
            if data[1] != username:
                file.write(item)
            else:
                harga = int(data[5])
                total_harga += harga
                items_to_remove.append(item)

    print(f"\nTotal pesanan Anda: {username}")

    biaya_admin = 3000
    harga_akhir = username + biaya_admin
    print(f"Biaya admin sebesar: {biaya_admin}")
    print(f"Anda harus membayar sebesar: {harga_akhir}")

    print("\nIngin bayar lewat apa?")
    print("1. Bayar dengan ShopeePay")
    print("2. Bayar dengan Dana")
    print("3. Kembali")

    choice = input("Pilihan: ")
    if choice == "1" or choice == "2":
        tanggal = datetime.date.today().strftime("%Y-%m-%d")
        waktu = datetime.datetime.now().strftime("%H:%M:%S")

        if choice == "1":
            pembayaran = "ShopeePay"
        elif choice == "2":
            pembayaran = "Dana"
        else:
            print("Pilihan tidak valid.")
            show_home(user_data)
            return

        histori_data = (histori_id, user_data, harga_akhir, tanggal, waktu, pembayaran)

        with open("histori.txt", "a") as file:
            file.write(",".join(str(data) for data in histori_data) + "\n")

        print("Pembayaran berhasil.")
        show_home(user_data)

        with open("keranjang.txt", "w") as file:
            for line in keranjang:
                if line not in items_to_remove:
                    file.write(line)

    elif choice == "3":
        show_home(user_data)
    else:
        print("Pilihan tidak valid.")

    show_home(user_data)


def show_histori(user_data, username):
    with open("histori.txt", "r") as file:
        histori = file.readlines()

    histori_found = False
    total_harga = 0

    for item in histori:
        data = item.strip().split(",")
        if data[1] == username:
            histori_found = True
            print(f"Anda melakukan transaksi sebesar: {data[2]}")
            print(f"tanggal: {data[3]}")
            print(f"waktu: {data[4]}")
            print(f"Via pembayaran: {data[5]}\n")
            harga = int(data[2])
            total_harga += harga
            print(f"Total transaksi anda saat ini: Rp.{total_harga}")

    if not histori_found:
        print("Anda belum melakukan transaksi apapun. Ayo checkout keranjang belanjaanmu! (tekan enter untuk kembali)")
        input()
        show_home(user_data)
        return

    print("1. Kembali")
    choice = input("Pilihan: ")
    if choice == "1":
        show_home(user_data)
    else:
        print("Pilihan tidak valid.")


def show_kantin(user_data, nama_kantin):
    with open("kantin.txt", "r") as file:
        kantin = file.readlines()

    warungs = []
    for item in kantin:
        data = item.strip().split(",")
        if data[1] == nama_kantin and data[2] not in warungs:
            warungs.append(data[2])

    print(f"\nPilihan Warung {nama_kantin}")
    for i, warung in enumerate(warungs):
        print(f"{i+1}. {warung}")

    print(f"{len(warungs)+1}. Kembali ke halaman Home")

    choice = input("Pilihan: ")
    if choice.isdigit() and int(choice) in range(1, len(warungs) + 1):
        nama_warung = warungs[int(choice) - 1]
        show_warung(user_data, nama_kantin, nama_warung)
    elif choice.isdigit() and int(choice) == len(warungs) + 1:
        show_home(user_data)
    else:
        print("Pilihan tidak valid.")
        show_kantin(user_data, nama_kantin)


def show_warung(user_data, nama_kantin, nama_warung):
    with open("kantin.txt", "r") as file:
        kantin = file.readlines()

    kategoris = []
    for item in kantin:
        data = item.strip().split(",")
        if data[1] == nama_kantin and data[2] == nama_warung and data[3] not in kategoris:
            kategoris.append(data[3])

    print(f"\nKategori {nama_warung}")
    for i, kategori in enumerate(kategoris):
        print(f"{i+1}. {kategori}")

    print(f"{len(kategoris)+1}. Kembali")

    choice = input("Pilihan: ")
    if choice.isdigit() and int(choice) in range(1, len(kategoris) + 1):
        kategori = kategoris[int(choice) - 1]
        show_menu(user_data, nama_kantin, nama_warung, kategori)
    elif choice.isdigit() and int(choice) == len(kategoris) + 1:
        show_kantin(user_data, nama_kantin)
    else:
        print("Pilihan tidak valid.")
        show_warung(user_data, nama_kantin, nama_warung)


def show_menu(user_data, nama_kantin, nama_warung, kategori):
    with open("kantin.txt", "r") as file:
        kantin = file.readlines()

    menus = []
    for item in kantin:
        data = item.strip().split(",")
        if data[1] == nama_kantin and data[2] == nama_warung and data[3] == kategori:
            menus.append(data)

    print(f"\nMenu {kategori}")
    for i, menu in enumerate(menus):
        print(f"{i+1}. Nama Menu: {menu[4]}, Harga: {menu[5]}")

    print()

    keranjang = []
    with open("keranjang.txt", "r") as file:
        keranjang_lines = file.readlines()
        if len(keranjang_lines) > 0:
            last_keranjang = keranjang_lines[-1].strip().split(",")
            id_keranjang = str(int(last_keranjang[0]) + 1)
        else:
            id_keranjang = "0"

    while True:
        print("Pilihan:")
        print("1. Tambah menu ke keranjang")
        print("2. Kembali")

        choice = input("Masukkan pilihan: ")
        if choice == "1":
            while True:
                menu_choice = input("Masukkan menu yang ingin ditambahkan ke keranjang: ")
                if menu_choice.isdigit() and int(menu_choice) in range(1, len(menus) + 1):
                    menu = menus[int(menu_choice) - 1]
                    keranjang.append((id_keranjang, user_data[4], nama_kantin, nama_warung, menu[4], menu[5]))
                    break
                else:
                    print("Maaf, inputan Anda salah. Silakan input ulang.")
            break
        elif choice == "2":
            show_warung(user_data, nama_kantin, nama_warung)
            return
        else:
            print("Maaf, pilihan tidak valid. Silakan input ulang.")

    with open("keranjang.txt", "a") as file:
        for item in keranjang:
            file.write(f"{item[0]},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]}\n")

    print("Menu berhasil ditambahkan ke keranjang. Cek keranjangmu untuk checkout.")
    show_home(user_data)


if __name__ == "__main__":
    main()
