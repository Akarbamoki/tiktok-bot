import os
import telebot
from yt_dlp import YoutubeDL

# تۆکنی بۆتەکەت لێرەدا جێگیر کراوە
BOT_TOKEN = "8861075342:AAGhh5gMYlGUJWkfrsdCbEoy47hRt9Q1jW4"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سڵاو! بەخێربێیت.\nتەنها لینکێکی ڤیدیۆیەکی تیکتۆکم بۆ بنێرە، منیش ڤیدیۆکەت بۆ دەنێرمەوە.")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text
    
    if "tiktok.com" not in url:
        bot.reply_to(message, "تکایە تەنها لینی تیکتۆکی ڕاست بنێرە. ⚠️")
        return

    msg = bot.reply_to(message, "کەمێک چاوەڕوان بە... ڤیدیۆکە ئامادە دەکرێت ⏳")
    
    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best',
        'quiet': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="فەرموو ڤیدیۆکەت پێشکەشە! ✨")
        
        os.remove('video.mp4')
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text("داوای لێبوردن دەکەم، کێشەیەک لە دابەزاندنی ڤیدیۆکەدا ڕوویدا. ❌", message.chat.id, msg.message_id)
        print(f"Error: {e}")

print("بۆتەکە بە سەرکەوتوویی کاری پێکرا...")
bot.infinity_polling()
