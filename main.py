import os
from flask import Flask
from threading import Thread
import telebot
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
print(f"TOKEN exists: {bool(BOT_TOKEN)}")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive ✅"

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🔥 BHF V2 خدام دابا!")

@bot.message_handler(func=lambda m: True)
def all_msg(msg):
    bot.reply_to(msg, f"وصلتني: {msg.text}")

def run_bot():
    while True:
        try:
            print("Starting bot polling...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port)
