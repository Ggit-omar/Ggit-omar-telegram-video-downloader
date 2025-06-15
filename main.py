import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# বট টোকেন ও চ্যানেল আইডি এখানে বসান
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel_username")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("🔍 ব্যবহার করুন: /search <movie name>")

    q = " ".join(context.args).lower()
    bot = context.bot

    try:
        async for msg in bot.get_chat(CHANNEL_ID).iter_history(limit=200):
            caption = msg.caption or msg.text or ""
            if msg.video and q in caption.lower():
                file_id = msg.video.file_id
                file = await bot.get_file(file_id)
                file_path = file.file_path
                link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                return await update.message.reply_text(
                    f"🎬 {caption}\n\n🔗 ডাউনলোড লিংক:\n{link}"
                )
        await update.message.reply_text("❌ মুভি খুঁজে পাওয়া যায়নি!")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("search", search))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
