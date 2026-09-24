                    SEEN_NEWS.add(entry.link)
                    now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
                    msg = f"🔥 عاجل 9/10 - Reuters\n{entry.title}\n\nالمصدر: Reuters\nالوقت: {now}\n{entry.link}"
                    # هنا حط الـ ID ديالك باش يوصلك فتيليجرام
                    bot.send_message(5723853263, msg)

            # Investing للاحتياط
            feed2 = feedparser.parse("https://www.investing.com/rss/news_25.rss")
            for entry in feed2.entries[:10]:
                if entry.link in SEEN_NEWS:
                    continue
                if any(w in entry.title.upper() for w in RED_WORDS):
                    SEEN_NEWS.add(entry.link)
                    now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
                    msg = f"🔥 عاجل 9/10 - Investing\n{entry.title}\n{entry.link}"
                    bot.send_message(5723853263, msg)

        except Exception as e:
            print(f"News error: {e}")
        time.sleep(15) # كيقلب كل 15 ثانية باش يبقى فايق وما ينعسش

# خدام فالخلفية
Thread(target=check_red_news_forever, daemon=True).start()

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Bot polling error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    run_bot()
