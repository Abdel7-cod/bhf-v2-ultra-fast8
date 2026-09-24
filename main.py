import os, time, threading
import feedparser, telebot
from flask import Flask
from datetime import datetime, timezone

TOKEN = "8205233186:AAE6w2BoPq4H1A2u3b4c5d6e7f8g9h0i1j2k"
CHAT = 5723853263

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
SEEN = set()

URLS = [
 "https://www.bls.gov/feed/bls_latest.rss",
 "http://feeds.reuters.com/reuters/businessNews",
 "https://www.federalreserve.gov/feeds/press_all.xml"
]

WORDS = ["CPI","NFP","PAYROLL","GDP","FOMC","FED"]

def check():
 print("V3 LIVE")
 while True:
  for url in URLS:
   try:
    feed = feedparser.parse(url)
    for e in feed.entries[:3]:
     if e.link in SEEN:
      continue
     if any(w in e.title.upper() for w in WORDS):
      SEEN.add(e.link)
      now = datetime.now(timezone.utc).strftime("%H:%M:%S")
      m = f"🔥 عاجل 9/10\n{e.title}\n{now} UTC\n{e.link}"
      bot.send_message(CHAT, m)
   except:
    pass
  time.sleep(5)

threading.Thread(target=check, daemon=True).start()

@app.route('/')
def home():
 return "V3 LIVE - 5s"

@bot.message_handler(commands=['start'])
def s(m):
 bot.reply_to(m, "✅ V3 خدام - 5s")

def run_f():
 app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_f, daemon=True).start()
bot.infinity_polling()
