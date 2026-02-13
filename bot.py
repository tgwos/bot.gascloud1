import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# 🔐 TOKEN
TOKEN = os.getenv("BOT_TOKEN")

# 🌐 URL
LOGO_URL = "https://tgwos.github.io/mini-app1/gas-cloud-logo.png"
CATALOG_URL = "https://tgwos.github.io/mini-app1/"

TELEGRAM_GROUP_URL = "https://t.me/+iMgIPdF4HPswMDRh"
SIGNAL_GROUP_URL = "https://signal.group/#CjQKIDujiZdq6QYIPqOVMwE8I2utpG27IFlHr3NcGuX9rg7nEhB5oZDrOOzWhaoX4bTSIZ4W"
REVIEWS_CHANNEL_URL = "https://t.me/+l_7fa3bXhGpjMTRh"

# 🔹 Tastiera principale
def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📦 Apri Catalogo",
                web_app=WebAppInfo(url=CATALOG_URL)
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Contatti ufficiali",
                callback_data="contacts"
            )
        ],
        [
            InlineKeyboardButton(
                "👥 Canale Telegram",
                url=TELEGRAM_GROUP_URL
            )
        ],
        [
            InlineKeyboardButton(
                "🔐 Gruppo Signal",
                url=SIGNAL_GROUP_URL
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Canale Recensioni",
                url=REVIEWS_CHANNEL_URL
            )
        ]
    ])

# 🔹 Tastiera indietro
def back_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⬅️ Indietro",
                callback_data="back"
            )
        ]
    ])

# 🔹 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=LOGO_URL,
        caption=(
            "WELCOME TO THE GAS CLOUD BOT!\n\n"
            "TO OPEN THE CATALOGUE PRESS ON THE MINI APP BUTTON."
        ),
        reply_markup=main_keyboard()
    )

# 🔹 Gestione pulsanti
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "contacts":
        await query.edit_message_caption(
            caption=(
                "📱 *CONTATTI UFFICIALI*\n\n"
                "✈️ *TELEGRAM*\n"
                "@GASCLOUD2\n\n"
                "📶 *SIGNAL*\n"
                "https://signal.me/#eu/CgfgU9UgZDG\\_PkIW19RZU90SY6WyRcInKywqHGpPorTDNai1pUFDc67sIUINOKeJ\n\n"
                "🥔 *POTATO*\n"
                "https://tutuduanyu.org/GASCLOUD2"
            ),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )

    elif query.data == "back":
        await query.edit_message_caption(
            caption=(
                "WELCOME TO THE GAS CLOUD BOT!\n\n"
                "TO OPEN THE CATALOGUE PRESS ON THE MINI APP BUTTON."
            ),
            reply_markup=main_keyboard()
        )

# 🔹 Avvio bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

# ✅ OBBLIGATORIO
if name == "__main__":
    main()
