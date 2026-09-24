import os
import time
import requests
import telebot
import threading
from bs4 import BeautifulSoup

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# خزن الناس اللي دارو /start باش نصيفط ليهم الأخبار
USERS = set()
SEEN = set()

URLS = {
    "BLS": "https://www.bls.gov/bls/news-release/",
    "FED": "https://www.federalreserve.gov/newsevents/pressreleases.htm",
    "Reuters": "https://www.reuters.com/business/"
}

WORDS = ["CPI", "NFP", "GDP", "FOMC", "FED", "INFLATION", "RATE", "POWELL"]

def check_news():
    print("V3 checker started - 5s")
    while True:
        try:
            for name, url in URLS.items():
                try:
                    r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                    text = r.text.upper()
                    for word in WORDS:
                        key = f"{name}-{word}-{r.text[:100]}"
                        # إلا بان خبر جديد فيه كلمة من WORDS
                        if word in text and key not in SEEN:
                            SEEN.add(key)
                            msg = f"🚨 V3 ALERT [{name}] 🚨\n💥 {word} لقيناها!\n🔗 {url}"
                            for user_id in USERS:
                                try:
                                    bot.send_message(user_id, msg)
                                except:
                                    pass
                            print(f"FOUND {word} in {name}")
                            break
                except Exception as e:
                    print(f"Error {name}: {e}")
        except Exception as e:
            print(f"Main loop error: {e}")
        
        time.sleep(5) # كل 5 ثواني كيفما بغيتي

@bot.message_handler(commands=['start'])
def start(m):
    USERS.add(m.chat.id)
    bot.reply_to(m, "✅ V3 خدام - 5s\nBLS + FED + Reuters\nCPI/NFP/GDP/FOMC كاينين")
    print(f"New user: {m.chat.id}")

# خدام فالخلفية
threading.Thread(target=check_news, daemon=True).start()

print("V3 LIVE - 5s checker")
bot.infinity_polling()
