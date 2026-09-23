import os
from flask import Flask
from threading import Thread
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "BHF V2 ULTRA FAST is running 24/7!"

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🔥 BHF V2 خدام 24/24 واخا تسد التيليفون!")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
