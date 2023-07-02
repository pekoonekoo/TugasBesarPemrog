import datetime


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
                    continue


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
                print("'{}' tersebut telah terpakai, silahkan coba kembali.".format(nim if data[2] == nim else username))
                break

        else:
            if len(users) > 0:
                last_user = users[-1].strip().split(",")
                id_user = str(int(last_user[0]) + 1)
            else:
                id_user = "0"

            with open("user.txt", "a") as file:
                file.write(f"{id_user},{nama_lengkap},{nim},{prodi},{username},{password}\n")

            print("Registrasi berhasil.")
            break


def show_home(user_data):
    print("\nSelamat datang di Kantin ITTP!")
    print("Mana pilihan kantinmu?")
    print("1. Kantin DC")
    print("2. Kantin TT")
    print("3. Lainnya")

    while True:
        choice = input("Pilihan: ")
        if choice == "1":
            show_kantin(user_data, "DC")
        elif choice == "2":
            show_kantin(user_data, "TT")
        elif choice == "3":
            show_lainnya(user_data)
        else:
            print("Pilihan tidak valid.")


def show_lainnya(user_data):
    print("\n1. Profil User")
    print("2. Keranjang")
    print("3. Histori Pesanan")
    print("4. Kembali ke halaman Home")
    print("5. Logout")

    choice = input("Pilihan: ")
    if choice == "1":
        show_profil(user_data)
    elif choice == "2":
        show_keranjang(user_data, user_data[4])
    elif choice == "3":
        show_histori(user_data, user_data[3])
    elif choice == "4":
        show_home(user_data)
    elif choice == "5":
        exit()
    else:
        print("Pilihan tidak valid.")
        show_lainnya(user_data)


def show_profil(user_data):
    print("\nProfil User")
    print(f"Nama Lengkap: {user_data[1]}")
    print(f"NIM: {user_data[2]}")
    print(f"Prodi: {user_data[3]}")
    print(f"Username: {user_data[4]}")
    print(f"Password: {user_data[5]}")

    print("\n1. Edit Profil")
    print("2. Kembali ke Home")

    choice = input("Pilihan: ")
    if choice == "1":
        edit_profil(user_data)
    elif choice == "2":
        show_home(user_data)
    else:
        print("Pilihan tidak valid.")


def edit_profil(user_data):
    print("\nEdit Profil")
    username = input("Username baru: ")
    password = input("Password baru: ")

    user_data[4] = username
    user_data[5] = password

    with open("user.txt", "r") as file:
        users = file.readlines()

    with open("user.txt", "w") as file:
        for user in users:
            user_info = user.strip().split(",")
            if user_info[0] == user_data[0]:
                file.write(f"{user_data[0]},{user_data[1]},{user_data[2]},{user_data[3]},"
                           f"{user_data[4]},{user_data[5]}\n")
            else:
                file.write(user)

    print("Profil berhasil diperbarui.")
    show_home(user_data)


def show_keranjang(user_data, username):
    with open("keranjang.txt", "r") as file:
        keranjang = file.readlines()

    keranjang_found = False
    total_harga = 0

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
            print()
            print(f"Total belanja anda: {total_harga}")

    if not keranjang_found:
        print("Keranjang belanja Anda kosong. (Klik enter untuk kembali ke halaman home)")
        input()
        show_home(user_data)
        return

    print("1. Checkout")
    print("2. Kembali")

    choice = input("Pilihan: ")
    if choice == "1":
        checkout(username, total_harga)
    elif choice == "2":
        show_home(user_data)
    else:
        print("Pilihan tidak valid.")


def checkout(user_data, username):
    with open("keranjang.txt", "r") as file:
        keranjang = file.readlines()

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
                total_harga += harga  # Menjumlahkan total harga pesanan
                items_to_remove.append(item)

    print(f"\nTotal pesanan anda: {username}")

    biaya_admin = 3000
    harga_akhir = username + biaya_admin
    print(f"Biaya admin sebesar: {biaya_admin}")
    print(f"Anda harus membayar sebesar: {harga_akhir}")

    print("\nIngin bayar lewat apa?")
    print("1. Bayar dengan ShopeePay")
    print("2. Bayar dengan Dana")

    choice = input("Pilihan: ")
    if choice == "1" or choice == "2":
        tanggal = datetime.date.today().strftime("%Y-%m-%d")  # Mendapatkan tanggal hari ini
        waktu = datetime.datetime.now().strftime("%H:%M:%S")  # Mendapatkan waktu saat ini

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

        with open("keranjang.txt", "w") as file:
            for line in keranjang:
                if line not in items_to_remove:
                    file.write(line)

    else:
        print("Pilihan tidak valid.")

    show_home(user_data)


def show_histori(user_data, username):
    with open("histori.txt", "r") as file:
        histori = file.readlines()

    histori_found = False

    for item in histori:
        data = item.strip().split(",")
        if len(data) >= 6 and data[1] == username:
            histori_found = True
            harga = data[2]
            tanggal = data[3]
            waktu = data[4]
            pembayaran = data[5]
            print(f"Anda melakukan transaksi sebesar: {harga}")
            print(f"tanggal: {tanggal}")
            print(f"waktu: {waktu}")
            print(f"Via pembayaran: {pembayaran}\n")

    if not histori_found:
        print("Anda belum melakukan transaksi apapun. Ayo checkout keranjang belanjaanmu! (tekan enter untuk kembali)")
        input()
        show_home(user_data)


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

    print(f"{len(kategoris)+1}. Kembali ke halaman Home")

    choice = input("Pilihan: ")
    if choice.isdigit() and int(choice) in range(1, len(kategoris) + 1):
        kategori = kategoris[int(choice) - 1]
        show_menu(user_data, nama_kantin, nama_warung, kategori)
    elif choice.isdigit() and int(choice) == len(kategoris) + 1:
        show_home(user_data)
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

    choice = input("Masukkan menu yang ingin ditambahkan ke keranjang: ")
    while choice.isdigit() and int(choice) in range(1, len(menus) + 1):
        menu = menus[int(choice) - 1]
        keranjang.append((id_keranjang, user_data[4], nama_kantin, nama_warung, menu[4], menu[5]))
        id_keranjang = str(int(id_keranjang) + 1)
        choice = input("Tekan enter")

    with open("keranjang.txt", "a") as file:
        for item in keranjang:
            file.write(f"{item[0]},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]}\n")

    print("Menu berhasil ditambahkan ke keranjang. Cek keranjangmu untuk checkout.")

    show_home(user_data)


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
        print("Registrasi berhasil. Silakan login.")
        main()
    else:
        print("Pilihan tidak valid.")
        main()


if __name__ == "__main__":
    main()
