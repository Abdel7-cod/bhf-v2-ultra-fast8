import os
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
print(f"DEBUG TOKEN: {TOKEN[:10] if TOKEN else 'NO TOKEN'}... len={len(TOKEN) if TOKEN else 0}")

if not TOKEN:
    raise ValueError("BOT_TOKEN ما كاينش!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "✅ V3 5 - خدام")

print("V3 LIVE - Check started")
bot.infinity_polling()
