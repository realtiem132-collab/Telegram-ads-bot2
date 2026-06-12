import os
from flask import Flask
import threading
import telebot
from telebot import types

TOKEN = '8078320470:AAHuBXNT7e2lv5VM9dCokKT0Hhj1PkNPK9E'
bot = telebot.TeleBot(TOKEN)
app = Flask('')

ADMIN_ID = 7867534011

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

user_ids = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_ids.add(message.chat.id)

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('📊 Market Analysis')
    btn2 = types.KeyboardButton('🧠 Trading Logic')
    btn3 = types.KeyboardButton('⚠️ Risk Management')
    markup.add(btn1, btn2, btn3)

    photo_url = 'https://raw.githubusercontent.com/realtiem132-collab/Bot-pic1/refs/heads/main/Gemini_Generated_Image_m6tstem6tstem6ts.png'

    caption = (
        "📚 QUOTEX TRADING EDUCATION BOT\n\n"
        "আপনাকে স্বাগতম! এই বটটি আপনাকে Quotex ট্রেডিং সম্পর্কে শিক্ষামূলক তথ্য প্রদান করে।\n\n"
        "✅ Market Analysis — কীভাবে বাজার বিশ্লেষণ করবেন\n"
        "✅ Trading Logic — সঠিক সিদ্ধান্ত নেওয়ার কৌশল\n"
        "✅ Risk Management — মূলধন সুরক্ষার নিয়মকানুন\n\n"
        "📌 ট্রেডিং শিখুন, সচেতন হন, সঠিকভাবে বিনিয়োগ করুন।\n\n"
        "আমাদের শিক্ষামূলক চ্যানেলে যোগ দিন:\n"
        "👇\n"
        "https://t.me/+swR7BhguPPQxZDc1\n"
        "https://t.me/+swR7BhguPPQxZDc1\n"
        "https://t.me/+swR7BhguPPQxZDc1\n\n"
        "👇 নিচের বাটন থেকে বিষয় বেছে নিন 👇"
    )

    bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup)

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ You are not authorized to use this command.")
        return

    text = message.text[len('/broadcast'):].strip()

    if not text:
        bot.send_message(message.chat.id, "⚠️ Please write a message after /broadcast\nExample: /broadcast Hello everyone!")
        return

    success = 0
    failed = 0
    for uid in user_ids:
        try:
            bot.send_message(uid, text)
            success += 1
        except Exception:
            failed += 1

    bot.send_message(message.chat.id, f"✅ Broadcast done!\n📤 Sent: {success}\n❌ Failed: {failed}")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_ids.add(message.chat.id)

    if message.text == '📊 Market Analysis':
        reply = (
            "📊 *Market Analysis — বাজার বিশ্লেষণ*\n\n"
            "সফল ট্রেডিংয়ের প্রথম ধাপ হলো বাজার সঠিকভাবে বিশ্লেষণ করা।\n\n"
            "*আমরা যা পর্যবেক্ষণ করি:*\n"
            "• Major currency pairs এবং OTC market\n"
            "• 1-minute candlestick chart — দ্রুত সিগন্যাল শনাক্তের জন্য\n"
            "• Bollinger Bands — মূল্যের সীমা বোঝার জন্য\n"
            "• Stochastic Oscillator — overbought/oversold চেনার জন্য\n"
            "• Keltner Channel — trend direction নির্ধারণে\n\n"
            "*মূল নীতি:*\n"
            "একটি indicator দিয়ে সিদ্ধান্ত নেবেন না।\n"
            "কমপক্ষে ২-৩টি indicator একসাথে confirm করলে তবেই trade নিন।\n\n"
            "📌 বিস্তারিত শিখতে চ্যানেলে যোগ দিন:\n"
            "https://t.me/+swR7BhguPPQxZDc1"
        )
        bot.send_message(message.chat.id, reply, parse_mode='Markdown')

    elif message.text == '🧠 Trading Logic':
        reply = (
            "🧠 *Trading Logic — সঠিক ট্রেডিং চিন্তাভাবনা*\n\n"
            "ট্রেডিং মানে শুধু buy/sell নয় — এটি একটি সুশৃঙ্খল প্রক্রিয়া।\n\n"
            "*মূল নিয়মসমূহ:*\n"
            "• Confirmation candle না দেখে কখনো trade নিবেন না\n"
            "• Trend-এর বিপরীতে trade এড়িয়ে চলুন\n"
            "• Support ও Resistance level চিহ্নিত করুন\n"
            "• Entry নেওয়ার আগে Exit plan তৈরি রাখুন\n\n"
            "*মানসিক শৃঙ্খলা:*\n"
            "• লসের পর revenge trade করবেন না\n"
            "• একটি trade-এ বেশি আবেগ লাগাবেন না\n"
            "• প্রতিটি trade-কে নতুনভাবে দেখুন\n\n"
            "*আমাদের প্রিমিয়াম সেটআপ:*\n"
            "সঠিক বিশ্লেষণের মাধ্যমে ৭০-৮০% নির্ভুলতা বজায় রাখা হয়।\n\n"
            "📌 আরও শিখতে চ্যানেলে যোগ দিন:\n"
            "https://t.me/+swR7BhguPPQxZDc1"
        )
        bot.send_message(message.chat.id, reply, parse_mode='Markdown')

    elif message.text == '⚠️ Risk Management':
        reply = (
            "⚠️ *Risk Management — মূলধন সুরক্ষার নিয়ম*\n\n"
            "একজন সফল trader সবার আগে তার capital রক্ষা করেন।\n\n"
            "*অবশ্যই মেনে চলুন:*\n"
            "• প্রতিটি trade-এ সর্বোচ্চ ১%-২% risk নিন\n"
            "• একসাথে একাধিক trade এড়িয়ে চলুন\n"
            "• Daily loss limit নির্ধারণ করুন — সীমা ছুঁলে বন্ধ করুন\n"
            "• Daily profit target পূরণ হলে আর trade করবেন না\n\n"
            "*সাধারণ ভুল যা এড়াবেন:*\n"
            "• লস কভার করতে বড় trade নেওয়া\n"
            "• Fast শেখার আগে real account-এ নামা\n"
            "• নিজের নিয়ম নিজে না মানা\n\n"
            "📌 সচেতন ট্রেডার হতে চ্যানেলে যোগ দিন:\n"
            "https://t.me/+swR7BhguPPQxZDc1"
        )
        bot.send_message(message.chat.id, reply, parse_mode='Markdown')

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.polling(none_stop=True)