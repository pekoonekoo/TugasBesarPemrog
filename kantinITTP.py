import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
    CallbackQueryHandler,
)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation states
STATUS, PEMILIK_DATA, MAHASISWA_DATA, PEMILIK_MENU, PEMILIK_EDIT, MAHASISWA_KANTIN, MAHASISWA_OUTLET, MAHASISWA_MENU = range(8)

# Global variables to store user data
user_data = {}

# Helper function to start the conversation
def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_text(
        f"Hallo {user.full_name}! Selamat datang di Kantin ITTP.\n"
        "Harap /daftar terlebih dahulu."
    )
    return STATUS

# Handler for the /daftar command
def daftar(update: Update, context: CallbackContext) -> int:
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Pemilik Outlet", callback_data='pemilik')],
        [InlineKeyboardButton("Mahasiswa", callback_data='mahasiswa')]
    ])
    update.message.reply_text("Silakan pilih status Anda:", reply_markup=reply_markup)
    return STATUS
(
            "Silakan masukkan data berikut:\n"
            "- Nama Lengkap\n"
            "- Nama Kantin\n"
            "- Nama Outlet\n"
            "- Nomor Telepon"
        )

# Handler for the status selection
def status_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    status = query.data
    user_data = context.user_data
    user_data['status'] = status

    if status == 'pemilik':
        query.message.reply_text(
            "Silakan masukkan data berikut:\n"
            "- Nama Lengkap\n"
            "- Nama Kantin\n"
            "- Nama Outlet\n"
            "- Nomor Telepon"
        )
        return PEMILIK_DATA
    elif status == 'mahasiswa':
        query.message.reply_text(
            "Silakan masukkan data berikut:\n"
            "- Nama Lengkap\n"
            "- NIM\n"
            "- Prodi\n"
            "- Email Pribadi"
        )
        return MAHASISWA_DATA
    else:
        query.message.reply_text("Status tidak valid. Silakan pilih status Anda kembali.")
        return STATUS


# Handler for pemilik data input
def pemilik_data(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    pemilik_data = update.message.text.split('\n')
    user_data['nama_lengkap'] = pemilik_data[0]
    user_data['nama_kantin'] = pemilik_data[1]
    user_data['nama_outlet'] = pemilik_data[2]
    user_data['nomor_telepon'] = pemilik_data[3]

    update.message.reply_text(
        f"Hallo {user_data['nama_lengkap']}, selamat datang di Kantin ITTP.\n"
        "Sebagai pemilik outlet, Anda dapat menggunakan bot ini dengan komando-komando berikut:\n"
        "/tambahmenu - Menambahkan menu baru\n"
        "/edit - Mengubah menu-menu yang tersedia di outlet Anda\n"
        "/main - Kembali ke menu utama\n"
        "/logout - Keluar dari program"
    )

    return ConversationHandler.END

# Handler for mahasiswa data input
def mahasiswa_data(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    mahasiswa_data = update.message.text.split('\n')
    user_data['nama_lengkap'] = mahasiswa_data[0]
    user_data['nim'] = mahasiswa_data[1]
    user_data['prodi'] = mahasiswa_data[2]
    user_data['email'] = mahasiswa_data[3]

    update.message.reply_text(
        f"Hallo {user_data['nama_lengkap']}, selamat datang di Kantin ITTP.\n"
        "Sebagai mahasiswa, Anda dapat menggunakan bot ini dengan komando-komando berikut:\n"
        "/pilihkantin - Melihat daftar kantin dan menu-menu mereka untuk dipilih\n"
        "/keranjangku - Melihat apa saja yang telah Anda masukkan ke keranjang belanja\n"
        "/checkout - Melakukan transaksi keranjangmu\n"
        "/main - Kembali menampilkan menu utama\n"
        "/logout - Keluar dari program"
    )

    return ConversationHandler.END

# Handler for the /tambahmenu command
def tambah_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Silakan masukkan nama menu:")
    return PEMILIK_MENU

# Handler for pemilik menu input
def pemilik_menu(update: Update, context: CallbackContext) -> int:
    menu_nama = update.message.text
    user_data.setdefault('menu', []).append(menu_nama)
    update.message.reply_text("Silakan masukkan harga menu:")
    return PEMILIK_EDIT

# Handler for editing menu
def edit_menu(update: Update, context: CallbackContext) -> int:
    menu_harga = update.message.text
    menu_id = len(user_data['menu']) - 1
    user_data['menu'][menu_id] = {
        'nama': user_data['menu'][menu_id],
        'harga': menu_harga
    }
    update.message.reply_text("Menu berhasil ditambahkan!")
    return ConversationHandler.END

# Handler for the /edit command
def edit(update: Update, context: CallbackContext) -> None:
    if 'menu' in user_data:
        keyboard = []
        for i, menu in enumerate(user_data['menu']):
            keyboard.append([InlineKeyboardButton(menu, callback_data=f'edit_{i}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Silakan pilih menu yang ingin diedit:",
            reply_markup=reply_markup
        )
        return PEMILIK_EDIT
    else:
        update.message.reply_text("Anda belum menambahkan menu. Silakan gunakan /tambahmenu untuk menambahkan menu.")
        return ConversationHandler.END

# Callback handler for editing menu selection
def edit_menu_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    menu_id = int(query.data.split('_')[1])
    user_data['edit_menu_id'] = menu_id

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Sunting", callback_data='sunting')],
        [InlineKeyboardButton("Hapus", callback_data='hapus')]
    ])
    query.edit_message_text(
        f"Menu: {user_data['menu'][menu_id]['nama']}\n"
        f"Harga: {user_data['menu'][menu_id]['harga']}\n"
        "Silakan pilih aksi:",
        reply_markup=keyboard
    )
    return PEMILIK_EDIT

# Callback handler for menu editing
def edit_menu_action(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    action = query.data

    if action == 'sunting':
        query.edit_message_text("Silakan masukkan nama menu baru:")
        return PEMILIK_MENU
    elif action == 'hapus':
        menu_id = user_data['edit_menu_id']
        del user_data['menu'][menu_id]
        query.edit_message_text("Menu berhasil dihapus!")
        return ConversationHandler.END

# Handler for the /main command
def main_menu(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Kembali ke menu utama.\n"
        "Silakan pilih salah satu perintah berikut sesuai dengan status Anda:"
    )
    if user_data['status'] == 'pemilik':
        update.message.reply_text(
            "/tambahmenu - Menambahkan menu baru\n"
            "/edit - Mengubah menu-menu yang tersedia di outlet Anda\n"
            "/main - Kembali ke menu utama\n"
            "/logout - Keluar dari program"
        )
    elif user_data['status'] == 'mahasiswa':
        update.message.reply_text(
            "/pilihkantin - Melihat daftar kantin dan menu-menu mereka untuk dipilih\n"
            "/keranjangku - Melihat apa saja yang telah Anda masukkan ke keranjang belanja\n"
            "/checkout - Melakukan transaksi keranjangmu\n"
            "/main - Kembali menampilkan menu utama\n"
            "/logout - Keluar dari program"
        )
    return STATUS

# Handler for the /logout command
def logout(update: Update, context: CallbackContext) -> int:
    user_data.clear()
    update.message.reply_text("Anda telah keluar dari program.")
    return ConversationHandler.END

# Handler for the /pilihkantin command
def pilih_kantin(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Berikut adalah daftar kantin yang tersedia:")
    # TODO: Display list of kantin and handle selection
    return MAHASISWA_KANTIN

# Handler for the /keranjangku command
def keranjangku(update: Update, context: CallbackContext) -> int:
    if 'keranjang' in user_data:
        keranjang = user_data['keranjang']
        total_harga = sum(menu['harga'] for menu in keranjang)
        keranjang_text = "Keranjang Belanja:\n"
        for i, menu in enumerate(keranjang):
            keranjang_text += f"{i+1}. {menu['nama']} - {menu['harga']} IDR\n"
        keranjang_text += f"Total: {total_harga} IDR"
        update.message.reply_text(keranjang_text)
    else:
        update.message.reply_text("Keranjang belanja Anda kosong.")
    return ConversationHandler.END

# Handler for the /checkout command
def checkout(update: Update, context: CallbackContext) -> int:
    if 'keranjang' in user_data:
        keranjang = user_data['keranjang']
        total_harga = sum(menu['harga'] for menu in keranjang)
        update.message.reply_text(f"Total harga keranjang: {total_harga} IDR")
        # TODO: Handle payment method selection
        return ConversationHandler.END
    else:
        update.message.reply_text("Keranjang belanja Anda kosong.")
        return ConversationHandler.END

def main() -> None:
    # Set up the Updater and Dispatcher
    updater = Updater("6153845817:AAFDOVs0Nfiurj_inPM2Df3RReWA0zPxeDI")
    dispatcher = updater.dispatcher

    # Conversation handler for the registration process
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('daftar', daftar)],
        states={
            STATUS: [CallbackQueryHandler(status_selection)],
            PEMILIK_DATA: [MessageHandler(Filters.text & ~Filters.command, pemilik_data)],
            MAHASISWA_DATA: [MessageHandler(Filters.text & ~Filters.command, mahasiswa_data)],
            PEMILIK_MENU: [MessageHandler(Filters.text & ~Filters.command, pemilik_menu)],
            PEMILIK_EDIT: [
                MessageHandler(Filters.text & ~Filters.command, edit_menu),
                CallbackQueryHandler(edit_menu_selection, pattern='^edit_'),
                CallbackQueryHandler(edit_menu_action, pattern='^(sunting|hapus)$'),
            ],
        },
        fallbacks=[CommandHandler('main', main_menu)],
    )

    # Add the handlers to the dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('logout', logout))
    dispatcher.add_handler(CommandHandler('tambahmenu', tambah_menu))
    dispatcher.add_handler(CommandHandler('edit', edit))
    dispatcher.add_handler(CommandHandler('pilihkantin', pilih_kantin))
    dispatcher.add_handler(CommandHandler('keranjangku', keranjangku))
    dispatcher.add_handler(CommandHandler('checkout', checkout))
    dispatcher.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()