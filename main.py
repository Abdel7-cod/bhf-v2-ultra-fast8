import os
import time
import requests
import telebot
import threading
from bs4 import BeautifulSoup

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN ما لقاهاش Render")

bot = telebot.TeleBot(TOKEN)

USERS = set()
SEEN = set()

URLS = {
    "BLS": "https://www.bls.gov/bls/news-release/",
    "FED": "https://www.federalreserve.gov/newsevents/pressreleases.htm",
    "Reuters": "https://www.reuters.com/business/",
}

WORDS = [
    "CPI",
    "NFP",
    "GDP",
    "FOMC",
    "FED",
    "INFLATION",
    "RATE",
    "POWELL",
]


def check_news():
    print("V3 checker started")

    while True:
        try:
            for name, url in URLS.items():
                try:
                    response = requests.get(
                        url,
                        timeout=15,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )

                    response.raise_for_status()

                    soup = BeautifulSoup(
                        response.text,
                        "html.parser"
                    )

                    text = soup.get_text(
                        " ",
                        strip=True
                    ).upper()

                    for word in WORDS:
                        key = f"{name}-{word}"

                        if word in text and key not in SEEN:
                            SEEN.add(key)

                            message = (
                                f"🚨 V3 ALERT [{name}] 🚨
"
                                f"💥 لقيت الكلمة: {word}
"
                                f"🔗 {url}"
                            )

                            for user_id in list(USERS):
                                try:
                                    bot.send_message(
                                        user_id,
                                        message
                                    )
                                except Exception as error:
                                    print(
                                        f"Telegram error: {error}"
                                    )

                            print(f"FOUND {word} in {name}")
                            break

                except Exception as error:
                    print(f"Error {name}: {error}")

        except Exception as error:
            print(f"Main loop error: {error}")

        time.sleep(60)


@bot.message_handler(commands=["start"])
def start(message):
    USERS.add(message.chat.id)

    bot.reply_to(
        message,
        "✅ البوت خدام
"
        "BLS + FED + Reuters
"
        "CPI/NFP/GDP/FOMC"
    )

    print(f"New user: {message.chat.id}")


threading.Thread(
    target=check_news,
    daemon=True
).start()

print("V3 LIVE")
bot.infinity_polling()
