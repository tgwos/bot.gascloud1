import os
import json
import asyncio
from pathlib import Path
from datetime import datetime

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

DATA_DIR = Path("/app/data")
USERS_FILE = DATA_DIR / "users.json"

ADMIN_IDS = {8679301783}  # IL TUO ID TELEGRAM

LOGO_URL = "https://tgwos.github.io/mini-app1/4985865506745158660.jpg"
CATALOG_URL = "https://tgwos.github.io/mini-app1/"

TELEGRAM_GROUP_URL = "https://t.me/+RC_zBHrK59RhMmJk"
SIGNAL_GROUP_URL = "https://signal.group/#CjQKIDujiZdq6QYIPqOVMwE8I2utpG27IFlHr3NcGuX9rg7nEhB5oZDrOOzWhaoX4bTSIZ4W"
REVIEWS_CHANNEL_URL = "https://t.me/+iJEzfG3m4BpjZjk0"
RISERVA_CHANNEL_URL = "https://t.me/+q15T2C4feBsxOTJh"


# ---------- STORAGE ----------

def load_users():
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not USERS_FILE.exists():
        return {}

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)

    temp_file = USERS_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    temp_file.replace(USERS_FILE)


async def register_user(update: Update):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return False

    users = load_users()
    key = str(user.id)
    now = datetime.utcnow().isoformat()

    old_data = users.get(key, {})

    users[key] = {
        "user_id": user.id,
        "chat_id": chat.id,
        "username": user.username or "",
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "language_code": user.language_code or "",
        "first_seen": old_data.get("first_seen", now),
        "last_seen": now,
        "blocked": old_data.get("blocked", False),
        "imported": old_data.get("imported", False),
    }

    save_users(users)
    return key not in old_data


# ---------- TASTI ----------

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


# ---------- BOT ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await register_user(update)

    await update.message.reply_photo(
        photo=LOGO_URL,
        caption="BENVENUTO",
        reply_markup=main_keyboard(),
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await register_user(update)

    if query.data == "contacts":
        await query.edit_message_caption(
            caption="CONTATTI:\n\n@GASCLOUD5\n\nCONTATTO\nSIGNAL:\nhttps://signal.me/#eu/CgfgU9UgZDG_PkIW19RZU90SY6WyRcInKywqHGpPorTDNai1pUFDc67sIUINOKeJ",
            reply_markup=back_keyboard(),
        )

    elif query.data == "back":
        await query.edit_message_caption(
            caption="BENVENUTO",
            reply_markup=main_keyboard(),
        )


# ---------- ADMIN ----------

async def import_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    users = load_users()

    text = update.message.text.replace("/import", "", 1).strip()

    if not text:
        await update.message.reply_text(
            "Uso:\n/import 👤 123456789\n👦🏻 Nome\n🌐 @username"
        )
        return

    lines = text.split("\n")

    current_id = None
    current_name = ""
    current_username = ""
    imported = 0
    updated = 0

    for line in lines:
        line = line.strip()

        if "👤" in line:
            digits = "".join(filter(str.isdigit, line))
            current_id = int(digits) if digits else None
            current_name = ""
            current_username = ""

        elif "👦🏻" in line:
            current_name = line.replace("👦🏻", "").strip()

        elif "🌐 @" in line:
            current_username = line.split("@", 1)[1].strip()

            if current_id:
                key = str(current_id)
                old_data = users.get(key, {})
                now = datetime.utcnow().isoformat()

                if key in users:
                    updated += 1
                else:
                    imported += 1

                users[key] = {
                    "user_id": current_id,
                    "chat_id": old_data.get("chat_id", current_id),
                    "username": current_username,
                    "first_name": current_name,
                    "last_name": old_data.get("last_name", ""),
                    "language_code": old_data.get("language_code", ""),
                    "first_seen": old_data.get("first_seen", now),
                    "last_seen": now,
                    "blocked": old_data.get("blocked", False),
                    "imported": True,
                }

    save_users(users)

    await update.message.reply_text(
        f"✅ Import completato\n\n"
        f"Nuovi utenti: {imported}\n"
        f"Aggiornati: {updated}\n"
        f"Totale salvati: {len(users)}"
    )


async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    users = load_users()

    if not users:
        await update.message.reply_text("Nessun utente salvato.")
        return

    with open(USERS_FILE, "rb") as f:
        await update.message.reply_document(
            document=f,
            filename="users.json",
            caption=f"Utenti salvati: {len(users)}"
        )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    users = load_users()

    total = len(users)
    blocked = sum(1 for u in users.values() if u.get("blocked"))
    active = total - blocked
    imported = sum(1 for u in users.values() if u.get("imported"))

    await update.message.reply_text(
        f"📊 Statistiche utenti\n\n"
        f"Totali: {total}\n"
        f"Attivi: {active}\n"
        f"Bloccati/falliti: {blocked}\n"
        f"Importati manualmente: {imported}"
    )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    if not context.args:
        await update.message.reply_text("Uso: /broadcast messaggio")
        return

    text = " ".join(context.args)
    users = load_users()

    if not users:
        await update.message.reply_text("Nessun utente salvato.")
        return

    await update.message.reply_text(f"Broadcast avviato verso {len(users)} utenti...")

    sent = 0
    failed = 0
    skipped = 0

    for uid, data in list(users.items()):
        if data.get("blocked") is True:
            skipped += 1
            continue

        try:
            await context.bot.send_message(
                chat_id=data["chat_id"],
                text=text
            )
            sent += 1
            await asyncio.sleep(0.05)

        except Exception:
            failed += 1
            users[uid]["blocked"] = True

    save_users(users)

    await update.message.reply_text(
        f"✅ Broadcast completato\n\n"
        f"Inviati: {sent}\n"
        f"Falliti/bloccati: {failed}\n"
        f"Saltati già bloccati: {skipped}"
    )


# ---------- AVVIO ----------

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN non trovato su Railway")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("import", import_users))
    app.add_handler(CommandHandler("export", export))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(buttons))

    print("BOT AVVIATO")
    print("USERS_FILE:", USERS_FILE.resolve())

    app.run_polling()


if __name__ == "__main__":
    main()
