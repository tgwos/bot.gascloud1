import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# URL diretto del logo (PNG/JPG)
LOGO_URL = "https://tgwos.github.io/mini-app1/gas-cloud-logo.png"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                text="📦 Apri Catalogo",
                web_app=WebAppInfo(
                    url="https://tgwos.github.io/mini-app1/"
                )
            )
        ]
    ]

    caption = (
        "WELCOME TO THE GAS CLOUD BOT!\n\n"
        "TO OPEN THE CATALOGUE PRESS ON THE MINI APP BUTTON."
    )

    await update.message.reply_photo(
        photo=LOGO_URL,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if name == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
