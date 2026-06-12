import os

import json

import threading

import telebot

from flask import Flask

from telebot import types



# ১. আপনার বটের টোকেন এবং নিজের টেলিগ্রাম আইডি এখানে বসান

TOKEN = '8078320470:AAGf7BJNwWMqWpalRr9sPe4EpQNTxh6WDQk'

ADMIN_ID = 7867534011  # এখানে @userinfobot থেকে পাওয়া আইডিটি বসান (কোনো উদ্ধৃতি চিহ্ন ছাড়া)



bot = telebot.TeleBot(TOKEN)

app = Flask('')



# মেম্বারদের আইডি স্থায়ীভাবে সেভ রাখার জন্য একটি ফাইল (যাতে বট রিস্টার্ট হলেও মেম্বার ডিলিট না হয়)

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



# /start কম্যান্ড হ্যান্ডলার (এখানে নতুন মেম্বারদের আইডি অটো সেভ হবে)

@bot.message_handler(commands=['start'])

def send_welcome(message):

    save_user(message.chat.id) # মেম্বার আইডি সেভ করা হলো

    

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    btn1 = types.KeyboardButton('Market Analysis')

    btn2 = types.KeyboardButton('🧠 Trading Logic')

    btn3 = types.KeyboardButton('⚠️ Risk Management')

    markup.add(btn1, btn2, btn3)

    

    welcome_text = "📊 Welcome to Educational Trading Bot!

আমরা আপনাকে শেখাই Professional Trading —
✅ Market Analysis
✅ Trading Logic & Strategy  
✅ Risk Management

নিচের মেনু থেকে শুরু করুন 👇"

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)



# /broadcast কম্যান্ড হ্যান্ডলার (শুধুমাত্র আপনার জন্য)

@bot.message_handler(commands=['broadcast'])

def broadcast_message(message):

    # চেক করা হচ্ছে মেসেজটি আপনি (অ্যাডমিন) পাঠিয়েছেন কিনা

    if message.from_user.id == ADMIN_ID:

        # কম্যান্ডের নামটুকু বাদ দিয়ে শুধু টেক্সটটুকু নেওয়া

        text_to_send = message.text.replace('/broadcast', '').strip()

        

        if not text_to_send:

            bot.reply_to(message, "ভাই, /broadcast লিখে স্পেস দিয়ে আপনার মেসেজ বা নোটিফিকেশনটি লিখুন।")

            return

            

        users_list = load_users()

        if not users_list:

            bot.reply_to(message, "এখনো বটে কোনো মেম্বার যুক্ত হয়নি ভাই।")

            return

            

        bot.reply_to(message, f"📢 মোট {len(users_list)} জন মেম্বারের কাছে নোটিফিকেশন পাঠানো শুরু হচ্ছে...")

        

        success_count = 0

        for user_id in users_list:

            try:

                bot.send_message(user_id, text_to_send)

                success_count += 1

            except Exception as e:

                pass # ইউজার যদি বট ব্লক করে দেয় তবে তাকে স্কিপ করবে

                

        bot.send_message(ADMIN_ID, f"✅ নোটিফিকেশন সফলভাবে {success_count} জন একটিভ মেম্বারের কাছে পৌঁছে গেছে!")

    else:

        bot.reply_to(message, "❌ দুঃখিত, এই কম্যান্ডটি শুধুমাত্র বটের আসল মালিকের জন্য।")



# বাটন ক্লিকের রিপ্লাই হ্যান্ডলার

@bot.message_handler(func=lambda message: True)

def handle_buttons(message):

    save_user(message.chat.id) # ইউজার মেসেজ দিলেও আইডি সেভ হবে

    

    if message.text == 'Market Analysis':

        reply = ("**📊 Market Analysis**\n\nWelcome to our Market Analysis section! We monitor major asset pairs and OTC markets.\n\n* **Style:** 1-minute candlestick charts for fast setups.\n* **Indicators:** Our tools leverage Bollinger Bands, Stochastic, and Keltner Channels.")

        bot.send_message(message.chat.id, reply, parse_mode='Markdown')

        

    elif message.text == '🧠 Trading Logic':

        reply = ("**🧠 Trading Logic**\n\nTrading is 10% strategy and 90% discipline.\n\n* **Rules:** Always wait for a clear confirmation candle.\n* **Accuracy:** Our premium setups maintain 70-80% accuracy to avoid market noise.")

        bot.send_message(message.chat.id, reply, parse_mode='Markdown')

        

    elif message.text == '⚠️ Risk Management':

        reply = ("**⚠️ Risk Management Rules**\n\nProtecting your capital is your number one job.\n\n* **Max Risk:** Never risk more than 1% to 2% per trade.\n* **Overtrading:** Set a daily profit and loss limit. Once hit, close the platform.")

        bot.send_message(message.chat.id, reply, parse_mode='Markdown')



if __name__ == "__main__":

    t = threading.Thread(target=run_flask)

    t.start()

    bot.polling(none_stop=True)
