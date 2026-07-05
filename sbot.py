import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# 1. Setup Flask for Render's health check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# 2. Setup your Telegram Bot
TOKEN = "8822357680:AAF36Vi7DNvxhyd0t1IV-L0Ka-aLob-iiEQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Welcome!\n"
        "💰 Is website se earning karne ke liye sabse pehle account banana zaroori hai.\n"
        "🔗 Step 1: Sign Up 👉 Sign up using this link: https://harday.co.in/login?ref=b4e58096-9266-4a0e-b8b2-4f1535bfcc86"
    )
    markup = InlineKeyboardMarkup()
    confirm_btn = InlineKeyboardButton("Ha maine sign up kr Liya hai", callback_data="confirmed_signup")
    markup.add(confirm_btn)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data == "confirmed_signup")
def handle_confirmation(call):
    final_message = "✅ Thank you for signing up! (Note: Replace this text with Shadab's final message)."
    bot.send_message(call.message.chat.id, final_message)
    bot.answer_callback_query(call.id)

# 3. Start both Flask and the Bot
if __name__ == "__main__":
    import threading
    
    # Run polling in a separate thread so it doesn't block Flask
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    
    # Render provides a PORT environment variable dynamically
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)