import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN or not CHANNEL_ID or ADMIN_ID == 0:
    raise ValueError("Missing environment variables. Please set BOT_TOKEN, CHANNEL_ID, ADMIN_ID in Railway.")
