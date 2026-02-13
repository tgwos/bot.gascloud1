import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "📦 Apri Catalogo",
            web_app=WebAppInfo(
                url="ggggggg"
            )
        )]
    ]

    await update.message.reply_text(
        "WELCOME TO THE SQUAD BCN OFFICIAL BOT!\n\n"
        "TO OPEN THE CATALOGUE PRESS ON THE MINI APP BUTTON.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if name == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
