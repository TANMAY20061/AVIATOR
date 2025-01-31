import time
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from flask import Flask
from multiprocessing import Process

# Bot Token
TOKEN = "7546442775:AAH-2qIYUPfG9Z7Do_PSSaSi9R5uKHtLtlc"

# Mandatory channel for verification
MANDATORY_CHANNEL = "@GODPREDICTION69"

# Additional displayed channels (not required for verification)
CHANNELS = {
    "🎊𝙈𝙊𝘿 𝘾𝙃𝘼𝙉𝙉𝙀𝙇🎊": "https://t.me/+xVHt9WSvAsw4YzY1",
    "⏳𝙋𝙍𝙀𝘿𝙄𝘾𝙏𝙄𝙊𝙉 𝘾𝙃𝘼𝙉𝙉𝙀𝙇⏳": f"https://t.me/{MANDATORY_CHANNEL[1:]}",  # Mandatory in the middle
    "👽2𝙉𝘿 𝙈𝙊𝘿 𝘾𝙃𝘼𝙉𝙉𝙀𝙇👽": "https://t.me/+RBaWtMQsKXU3MTJl",
    "🐍𝘽𝘼𝘿𝙎𝙃𝘼𝙃 𝘽𝘼𝘾𝘾𝙃𝘼🐍": "https://t.me/+s9eHruWKORg5YTU1",
}

# Public Telegram channel image link
IMAGE_URL = "https://t.me/PREDICTIONZRX/4"

# Cooldown duration (seconds)
COOLDOWN_TIME = 40
last_prediction_time = {}

# Convert time to 12-hour format
def get_time():
    return datetime.now().strftime("%I:%M:%S %p")

# Check if user is a member of @GODPREDICTION69
async def is_user_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(MANDATORY_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# Send "Join Channels" message
async def send_join_message(update):
    # Displaying all channels with unique labels
    keyboard = [
        [InlineKeyboardButton(name, url=link)] for name, link in CHANNELS.items()
    ]
    keyboard.append([InlineKeyboardButton("✅ JOINED", callback_data="joined")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "🚀 <b>𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙩𝙝𝙚 𝘼𝙑𝙄𝘼𝙏𝙊𝙍 𝙎𝙄𝙂𝙉𝘼𝙇 𝘽𝙤𝙩!</b>\n\n"
        "🔴 <b>𝙁𝙤𝙡𝙡𝙤𝙬 𝙩𝙝𝙚𝙨𝙚 𝙨𝙩𝙚𝙥𝙨 𝙩𝙤 𝙘𝙤𝙣𝙩𝙞𝙣𝙪𝙚:</b>\n"
        "1️⃣ 𝙅𝙤𝙞𝙣 𝙩𝙝𝙚 <b>MUST JOIN</b> 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 📢\n"
        "2️⃣ 𝐂𝐥𝐢𝐜𝐤 𝐭𝐡𝐞 '✅ 𝐉𝐎𝐈𝐍𝐄𝐃' button\n\n"
        "🔒 <b>𝘼𝙘𝙘𝙚𝙨𝙨 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙜𝙧𝙖𝙣𝙩𝙚𝙙 𝙤𝙣𝙡𝙮 𝙖𝙛𝙩𝙚𝙧 𝙫𝙚𝙧𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣!</b>"
    )

    await update.message.reply_text(message, parse_mode="HTML", reply_markup=reply_markup)

# /start command
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if await is_user_member(user_id, context):
        await update.message.reply_text(
            "✅ 𝐘𝐨𝐮 𝐚𝐫𝐞 𝐯𝐞𝐫𝐢𝐟𝐢𝐞𝐝! 𝐓𝐚𝐩 '🎯 𝐆𝐄𝐓 𝐏𝐑𝐄𝐃𝐈𝐂𝐓𝐈𝐎𝐍' 𝐭𝐨 𝐫𝐞𝐜𝐞𝐢𝐯𝐞 𝐬𝐢𝐠𝐧𝐚𝐥𝐬.", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 𝙂𝙀𝙏 𝙋𝙍𝙀𝘿𝙄𝘾𝙏𝙄𝙊𝙉", callback_data="predict")]])
        )
    else:
        await send_join_message(update)

# Handle "JOINED ✅" button
async def joined_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_user_member(user_id, context):
        await query.message.edit_text(
            "🎉 <b>𝙑𝙚𝙧𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡!</b>\n\n"             
            "✅ 𝙔𝙤𝙪 𝙘𝙖𝙣 𝙣𝙤𝙬 𝙜𝙚𝙩 𝙥𝙧𝙚𝙙𝙞𝙘𝙩𝙞𝙤𝙣𝙨.\n"             
            "🔮 𝘾𝙡𝙞𝙘𝙠 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣 𝙗𝙚𝙡𝙤𝙬 𝙩𝙤 𝙧𝙚𝙘𝙚𝙞𝙫𝙚 𝙮𝙤𝙪𝙧 𝙛𝙞𝙧𝙨𝙩 𝙨𝙞𝙜𝙣𝙖𝙡!\n\n"             
            "📢 <i>𝙎𝙩𝙖𝙮 𝙩𝙪𝙣𝙚𝙙 𝙛𝙤𝙧 𝙖𝙘𝙘𝙪𝙧𝙖𝙩𝙚 𝙨𝙞𝙜𝙣𝙖𝙡𝙨!</i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 𝙂𝙀𝙏 𝙋𝙍𝙀𝘿𝙄𝘾𝙏𝙄𝙊𝙉", callback_data="predict")]])
        )
    else:
        await query.answer("❌ 𝙔𝙤𝙪 𝙝𝙖𝙫𝙚𝙣'𝙩 𝙟𝙤𝙞𝙣𝙚𝙙 𝙩𝙝𝙚 𝙧𝙚𝙦𝙪𝙞𝙧𝙚𝙙 𝙘𝙝𝙖𝙣𝙣𝙚𝙡!", show_alert=True)

# Generate stylish prediction message
def get_prediction():
    signal = round(random.uniform(1.0, 10.0), 1)
    return (
        f"⏳ <b>𝘽𝙚𝙩 𝙏𝙞𝙢𝙚:</b> <code>{get_time()}</code>\n\n"
        f"📢 <b>𝙎𝙞𝙜𝙣𝙖𝙡:</b> <tg-spoiler>{signal}</tg-spoiler>\n\n"
        f"🔥 <i>𝙈𝙖𝙙𝙚 𝙗𝙮 @𝙩𝙖𝙣𝙢𝙖𝙮𝙥𝙖𝙪𝙡21</i> 🔥"
    )

# Handle "🎯 GET PREDICTION" button
async def prediction_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if not await is_user_member(user_id, context):
        await send_join_message(query)
        return

    if user_id not in last_prediction_time or time.time() - last_prediction_time[user_id] >= COOLDOWN_TIME:
        last_prediction_time[user_id] = time.time()

        keyboard = [[InlineKeyboardButton("𝙉𝙚𝙭𝙩 𝙋𝙧𝙚𝙙𝙞𝙘𝙩𝙞𝙤𝙣", callback_data="predict")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_photo(
            photo=IMAGE_URL,
            caption=get_prediction(),
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    else:
        remaining_time = int(COOLDOWN_TIME - (time.time() - last_prediction_time[user_id]))
        await query.answer(f"⏳ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩 {remaining_time} seconds.", show_alert=True)

# Flask App Initialization
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "Flask server is running successfully!"

# Function to Start the Flask App
def start_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(joined_callback, pattern="joined"))
    app.add_handler(CallbackQueryHandler(prediction_callback, pattern="predict"))

    # Start Flask server in a separate process
    flask_process = Process(target=start_flask)
    flask_process.start()

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
