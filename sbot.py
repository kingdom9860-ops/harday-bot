import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading

# 1. Setup Flask for Render's health check (keeps it online)
app = Flask(__name__)

@app.route('/')
def home():
    return "Therlooter_bot is running!"

# 2. Your specific Telegram Bot Token
TOKEN = "8958560245:AAGWItieHLJ_QQZH1PFGe9VvKf5-rXlcAmI"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # The exact message text requested
    welcome_text = (
        "Welcome!\n"
        "Is website se earning karne ke liye sabse pehle account banana zaroori hai.\n"
        "Step 1: Sign Up  Sign up using this link: https://harday.co.in/login?ref=b4e58096-9266-4a0e-b8b2-4f1535bfcc86"
    )
    
    # The confirmation button
    markup = InlineKeyboardMarkup()
    confirm_btn = InlineKeyboardButton("Ha maine sign up kr Liya hai", callback_data="confirmed_signup")
    markup.add(confirm_btn)
    
    # Sends the message
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data == "confirmed_signup")
def handle_confirmation(call):
    # The reply after they click the button
    final_message = "✅ Thank you for signing up!"
    bot.send_message(call.message.chat.id, final_message)
    bot.answer_callback_query(call.id)

# 3. Start everything
if __name__ == "__main__":
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
