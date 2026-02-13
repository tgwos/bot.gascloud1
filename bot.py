import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

LOGO_URL = "https://tgwos.github.io/mini-app1/gas-cloud-logo.png"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            text="📦 Apri Catalogo",
            web_app=WebAppInfo(url="https://tgwos.github.io/mini-app1/")
        )
    ]]

    await update.message.reply_photo(
        photo=LOGO_URL,
        caption=(
            "WELCOME TO THE GAS CLOUD BOT!\n\n"
            "TO OPEN THE CATALOGUE PRESS ON THE MINI APP BUTTON."
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
