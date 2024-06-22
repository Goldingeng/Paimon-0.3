import telebot

TOKEN = '7038000405:AAFfayc0Rvq1qLGquomo9nZ3vE_RYoCIyXI'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo_id = message.photo[-1].file_id  # Получаем ID последней (самой большой) фотографии
    bot.reply_to(message, f"Received photo ID: {photo_id}")

bot.polling()