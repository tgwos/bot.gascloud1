import os
import json
import asyncio
from pathlib import Path
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
DATA_DIR = Path("/app/data") if Path("/app/data").exists() else Path(".")
USERS_FILE = DATA_DIR / "users.json"

ADMIN_IDS = {123456789}  # METTI IL TUO ID

LOGO_URL = "https://tgwos.github.io/mini-app1/4985865506745158660.jpg"
CATALOG_URL = "https://tgwos.github.io/mini-app1/"

TELEGRAM_GROUP_URL = "https://t.me/+RC_zBHrK59RhMmJk"
SIGNAL_GROUP_URL = "https://signal.group/#CjQKIDujiZdq6QYIPqOVMwE8I2utpG27IFlHr3NcGuX9rg7nEhB5oZDrOOzWhaoX4bTSIZ4W"
REVIEWS_CHANNEL_URL = "https://t.me/+iJEzfG3m4BpjZjk0"
RISERVA_CHANNEL_URL = "https://t.me/+Aaw_vDmJbUc5NWFh"


def load_users():
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


async def register_user(update: Update):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return False

    users = load_users()
    key = str(user.id)
    is_new = key not in users

    users[key] = {
        "chat_id": chat.id,
        "username": user.username or "",
    }

    save_users(users)
    return is_new


# ---------- BOT ----------

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Apri Catalogo", web_app=WebAppInfo(url=CATALOG_URL))],
        [InlineKeyboardButton("📞 Contatti ufficiali", callback_data="contacts")],
        [InlineKeyboardButton("👥 Canale Telegram", url=TELEGRAM_GROUP_URL)],
        [InlineKeyboardButton("🔐 Gruppo Signal", url=SIGNAL_GROUP_URL)],
        [InlineKeyboardButton("⭐ Recensioni", url=REVIEWS_CHANNEL_URL)],
        [InlineKeyboardButton("🔹 Riserva", url=RISERVA_CHANNEL_URL)],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Indietro", callback_data="back")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await register_user(update)
    await update.message.reply_photo(
        photo=LOGO_URL,
        caption="BENVENUTO",
        reply_markup=main_keyboard(),
    )


# ---------- ADMIN ----------

async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    with open(USERS_FILE, "rb") as f:
        await update.message.reply_document(f)


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    if not context.args:
        await update.message.reply_text("Uso: /broadcast messaggio")
        return

    text = " ".join(context.args)
    users = load_users()

    sent = 0
    failed = 0

    for uid, data in list(users.items()):
        try:
            await context.bot.send_message(data["chat_id"], text)
            sent += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1
            users.pop(uid, None)  # rimuove utenti morti

    save_users(users)

    await update.message.reply_text(f"Inviati: {sent} | Rimossi: {failed}")


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "contacts":
        await query.edit_message_caption(
            caption="CONTATTI:\n@GASCLOUD4",
            reply_markup=back_keyboard(),
        )
    elif query.data == "back":
        await query.edit_message_caption(
            caption="BENVENUTO",
            reply_markup=main_keyboard(),
        )


# ---------- START ----------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("export", export))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()


if __name__ == "__main__":
    main()

