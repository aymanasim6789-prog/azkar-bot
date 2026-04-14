import telebot
import random
import threading
import time
from telebot import types
from config import TOKEN, ADMINS

bot = telebot.TeleBot(TOKEN)

# ======================
# 🔐 أدمن
# ======================
def is_admin(user_id):
    return user_id in ADMINS

# ======================
# 📋 القائمة (Inline)
# ======================
def menu():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.row(
        types.InlineKeyboardButton("📿 ذكر", callback_data="zekr"),
        types.InlineKeyboardButton("📖 حديث", callback_data="hadith")
    )

    keyboard.row(
        types.InlineKeyboardButton("🤲 دعاء", callback_data="dua"),
        types.InlineKeyboardButton("📜 آية", callback_data="ayah")
    )

    keyboard.row(
        types.InlineKeyboardButton("💚 صلاة 50", callback_data="salat50"),
        types.InlineKeyboardButton("💙 صلاة 100", callback_data="salat100")
    )

    keyboard.row(
        types.InlineKeyboardButton("🌙 إبراهيمية", callback_data="ibrahim")
    )

    return keyboard

# ======================
# 📿 أذكار + أحاديث + أدعية + آيات (نفسك)
# ======================
azkar = ([
    "سُبْحَانَ اللَّهِ 🌿",
    "الْحَمْدُ لِلَّهِ 🤍",
    "اللَّهُ أَكْبَرُ 🔥",
    "لَا إِلٰهَ إِلَّا اللَّهُ ☁️",
    "أَسْتَغْفِرُ اللَّهَ 🤲",
] * 10)[:50]

hadiths = ([
    "إنما الأعمال بالنيات 🤍 (البخاري ومسلم)",
    "الدين النصيحة 📖 (مسلم)",
    "لا تغضب ⚡ (البخاري)",
    "تبسمك في وجه أخيك صدقة 😊 (الترمذي)",
] * 13)[:50]

duas = ([
    "اللَّهُمَّ اغْفِرْ لِي 🤲",
    "اللَّهُمَّ ارْحَمْنِي 💚",
    "اللَّهُمَّ اهْدِنِي 🌿",
    "اللَّهُمَّ ارْزُقْنِي 🌸",
] * 13)[:50]

ayat = ([
    "﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾ 🌿",
    "﴿اللَّهُ غَفُورٌ رَحِيمٌ﴾ 💚",
    "﴿وَاذْكُرُوا اللَّهَ كَثِيرًا﴾ 🤍",
] * 17)[:50]

# ======================
# 💚 الصلاة على النبي
# ======================
salat_50 = "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ ﷺ 💚\n" * 50
salat_100 = "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ ﷺ 💙\n" * 100

ibrahimiyya = """🌙 الصلاة الإبراهيمية:

اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ،
كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ،
إِنَّكَ حَمِيدٌ مَجِيدٌ 💚
"""

# ======================
# 🚀 AUTO MESSAGE (هذا الجديد)
# ======================
def auto_send():
    while True:
        for admin in ADMINS:
            try:
                bot.send_message(admin, random.choice(azkar))
            except:
                pass
        time.sleep(60)  # كل دقيقة

# تشغيل التلقائي
threading.Thread(target=auto_send, daemon=True).start()

# ======================
# 🚀 Start
# ======================
@bot.message_handler(commands=["start"])
def start(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ للأدمن فقط")
        return

    bot.send_message(
        message.chat.id,
        "👑 أهلاً بك في بوت الأذكار",
        reply_markup=menu()
    )

# ======================
# 🎛️ Callback
# ======================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id

    if call.data == "zekr":
        bot.send_message(chat_id, random.choice(azkar))

    elif call.data == "hadith":
        bot.send_message(chat_id, random.choice(hadiths))

    elif call.data == "dua":
        bot.send_message(chat_id, random.choice(duas))

    elif call.data == "ayah":
        bot.send_message(chat_id, random.choice(ayat))

    elif call.data == "salat50":
        bot.send_message(chat_id, salat_50)

    elif call.data == "salat100":
        bot.send_message(chat_id, salat_100)

    elif call.data == "ibrahim":
        bot.send_message(chat_id, ibrahimiyya)

    bot.answer_callback_query(call.id)

# ======================
print("🔥 Bot is running...")
bot.infinity_polling()
