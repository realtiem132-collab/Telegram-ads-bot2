import os
import json
import threading
import telebot
from flask import Flask
from telebot import types

# ১. আপনার বটের টোকেন এবং নিজের টেলিগ্রাম আইডি এখানে বসান
TOKEN = '8078320470:AAHuBXNT7e2lv5VM9dCokKT0Hhj1PkNPK9E'
ADMIN_ID = 7867534011  # এখানে @userinfobot থেকে পাওয়া আইডিটি বসান (কোনো উদ্ধৃতি চিহ্ন ছাড়া)

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# মেম্বারদের আইডি স্থায়ীভাবে সেভ রাখার জন্য একটি ফাইল (যাতে বট রিস্টার্ট হলেও মেম্বার ডিলিট না হয়)
USER_FILE = "bot_users.json"

def load_users():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.add(user_id)
        with open(USER_FILE, "w") as f:
            json.dump(list(users), f)

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# /start কম্যান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id)

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('📊 Market Analysis')
    btn2 = types.KeyboardButton('🧠 Trading Logic')
    btn3 = types.KeyboardButton('⚠️ Risk Management')
    markup.add(btn1, btn2, btn3)

    welcome_text = (
        "📊 *Welcome to Educational Trading Bot!*\n\n"
        "আমরা আপনাকে শেখাই Professional Trading —\n"
        "✅ Market Analysis\n"
        "✅ Trading Logic & Strategy\n"
        "✅ Risk Management\n\n"
        "নিচের মেনু থেকে শুরু করুন 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# /help কম্যান্ড হ্যান্ডলার
@bot.message_handler(commands=['help'])
def send_help(message):
    save_user(message.chat.id)
    help_text = (
        "ℹ️ *Help & Info*\n\n"
        "এই bot টি সম্পূর্ণ Educational Trading শেখার জন্য।\n\n"
        "📌 *Available Commands:*\n"
        "/start — Main Menu\n"
        "/help — এই message\n\n"
        "📌 *Available Sections:*\n"
        "📊 Market Analysis — Chart & Indicator শেখা\n"
        "🧠 Trading Logic — Strategy & Rules\n"
        "⚠️ Risk Management — টাকা সুরক্ষার নিয়ম\n\n"
        "📢 *আমাদের Main Channel:*\n"
        "https://t.me/+gR00nolNZmA2MGQ1\n"
        "https://t.me/+gR00nolNZmA2MGQ1\n\n"
        "❓ কোনো প্রশ্ন থাকলে channel-এ message করুন।"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# /broadcast কম্যান্ড হ্যান্ডলার (শুধুমাত্র আপনার জন্য)
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id == ADMIN_ID:
        text_to_send = message.text.replace('/broadcast', '').strip()

        if not text_to_send:
            bot.reply_to(message, "ভাই, /broadcast লিখে স্পেস দিয়ে আপনার মেসেজ বা নোটিফিকেশনটি লিখুন।")
            return

        users_list = load_users()
        if not users_list:
            bot.reply_to(message, "এখনো বটে কোনো মেম্বার যুক্ত হয়নি ভাই।")
            return

        bot.reply_to(message, f"📢 মোট {len(users_list)} জন মেম্বারের কাছে নোটিফিকেশন পাঠানো শুরু হচ্ছে...")

        success_count = 0
        for user_id in users_list:
            try:
                bot.send_message(user_id, text_to_send)
                success_count += 1
            except Exception as e:
                pass

        bot.send_message(ADMIN_ID, f"✅ নোটিফিকেশন সফলভাবে {success_count} জন একটিভ মেম্বারের কাছে পৌঁছে গেছে!")
    else:
        bot.reply_to(message, "❌ দুঃখিত, এই কম্যান্ডটি শুধুমাত্র বটের আসল মালিকের জন্য।")

# বাটন ক্লিকের রিপ্লাই হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    save_user(message.chat.id)

    if message.text == '📊 Market Analysis':
        reply = (
            "📈 *Market Analysis*\n\n"
            "আমরা প্রতিদিন Major Asset Pairs এবং OTC Market monitor করি।\n\n"
            "🕯 *Chart Style:* 1-minute Candlestick\n\n"
            "🔧 *Indicators আমরা ব্যবহার করি:*\n\n"
            "• *Bollinger Bands* — market volatility বোঝার জন্য\n"
            "• *Stochastic Oscillator* — overbought/oversold চেনার জন্য\n"
            "• *Keltner Channel* — trend direction নির্ধারণে\n\n"
            "📌 *কীভাবে analysis পড়বেন?*\n"
            "▪️ Price Bollinger Band-এর উপরে → সম্ভাব্য DOWN\n"
            "▪️ Price নিচে গেলে → সম্ভাব্য UP\n"
            "▪️ Stochastic 80+ = Overbought\n"
            "▪️ Stochastic 20- = Oversold\n\n"
            "📢 Daily analysis পেতে join করুন:\n"
            "👉 t.me/education\_trading\_t"
        )
        bot.send_message(message.chat.id, reply, parse_mode='Markdown')

    elif message.text == '🧠 Trading Logic':
        reply = (
            "🧠 *Trading Logic*\n\n"
            "সফল trader হতে হলে Logic দিয়ে trade করতে হয়, emotion দিয়ে নয়।\n\n"
            "📌 *আমাদের Trading Rules:*\n\n"
            "1️⃣ *Trend Follow করুন*\n"
            "   — Higher High, Higher Low = Uptrend\n"
            "   — Lower High, Lower Low = Downtrend\n\n"
            "2️⃣ *Confirmation ছাড়া Entry নয়*\n"
            "   — কমপক্ষে ২টা indicator একমত হলে তবেই enter করুন\n\n"
            "3️⃣ *একটা trade-এ সব টাকা নয়*\n"
            "   — প্রতি trade-এ মোট balance-এর max ৫% ব্যবহার করুন\n\n"
            "4️⃣ *Loss হলে revenge trade নয়*\n"
            "   — থামুন, বিশ্রাম নিন, আবার analyze করুন\n\n"
            "💡 *মনে রাখুন:* Best traders দিনে ৩-৫টার বেশি trade করেন না।"
        )
        bot.send_message(message.chat.id, reply, parse_mode='Markdown')

    elif message.text == '⚠️ Risk Management':
        reply = (
            "⚠️ *Risk Management*\n\n"
            "Trading-এ টিকে থাকার একমাত্র উপায় — Risk নিয়ন্ত্রণ।\n\n"
            "📌 *Golden Rules:*\n\n"
            "1️⃣ *1% Rule*\n"
            "   — প্রতি trade-এ account-এর ১% এর বেশি risk নেবেন না\n"
            "   — Balance ৳10,000 হলে, প্রতি trade-এ max ৳100\n\n"
            "2️⃣ *Stop Loss সবসময় দিন*\n"
            "   — Stop Loss ছাড়া trade = জুয়া\n\n"
            "3️⃣ *Risk:Reward Ratio মানুন*\n"
            "   — Minimum 1:2 — ১০০ টাকা risk করলে ২০০ টাকা target\n\n"
            "4️⃣ *Daily Loss Limit*\n"
            "   — দিনে ৩টা loss হলে সেদিনের মতো বন্ধ করুন\n\n"
            "5️⃣ *Martingale থেকে সাবধান*\n"
            "   — Double করার strategy account শেষ করে দেয়\n\n"
            "💡 *Pro Tip:* আগে Demo account-এ practice করুন, তারপর Real-এ আসুন।"
        )
        bot.send_message(message.chat.id, reply, parse_mode='Markdown')

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.polling(none_stop=True)
