import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))
APPROVED_FILE = "approved_channels.txt"

def is_channel_approved(channel_id: str) -> bool:
    if not os.path.exists(APPROVED_FILE):
        return False
    with open(APPROVED_FILE, "r") as f:
        return channel_id.strip() in [line.strip() for line in f.readlines()]

def approve_channel(channel_id: str):
    with open(APPROVED_FILE, "a") as f:
        f.write(channel_id.strip() + "\n")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return await update.message.reply_text("❌ আপনি অনুমোদিত অ্যাডমিন নন।")

    if not context.args:
        return await update.message.reply_text("📌 ব্যবহার করুন: /approve <channel_id>")

    channel_id = context.args[0]
    if is_channel_approved(channel_id):
        return await update.message.reply_text("✅ এই চ্যানেল আগেই অনুমোদিত হয়েছে।")

    approve_channel(channel_id)
    await update.message.reply_text(f"✅ চ্যানেল {channel_id} অনুমোদিত হয়েছে।")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("🔍 ব্যবহার করুন: /search <movie name>")

    bot = context.bot

    try:
        chat = await bot.get_chat(os.getenv("CHANNEL_ID"))
        channel_id = str(chat.id)

        if not is_channel_approved(channel_id):
            msg = (
                f"📢 নতুন চ্যানেল ডিটেক্ট করা হয়েছে:\n"
                f"📌 Title: {chat.title}\n"
                f"🆔 Channel ID: `{channel_id}`\n\n"
                f"✅ অনুমোদনের জন্য লিখুন:\n"
                f"/approve {channel_id}"
            )
            await bot.send_message(chat_id=GROUP_ID, text=msg, parse_mode="Markdown")
            return await update.message.reply_text("🚫 এই চ্যানেল এখনো অনুমোদিত নয়।")

    except Exception as e:
        return await update.message.reply_text(f"⚠️ Error: {e}")

    # Proceed to search
    q = " ".join(context.args).lower()
    try:
        async for msg in bot.get_chat(os.getenv("CHANNEL_ID")).iter_history(limit=200):
            caption = msg.caption or msg.text or ""
            if msg.video and q in caption.lower():
                file_id = msg.video.file_id
                file = await bot.get_file(file_id)
                link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
                return await update.message.reply_text(
                    f"🎬 {caption}\n\n🔗 ডাউনলোড:\n{link}"
                )
        await update.message.reply_text("❌ মুভি খুঁজে পাওয়া যায়নি!")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("approve", approve))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
