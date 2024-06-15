import telebot

TOKEN = '7038000405:AAFfayc0Rvq1qLGquomo9nZ3vE_RYoCIyXI'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo_id = message.photo[-1].file_id  # Получаем ID последней (самой большой) фотографии
    bot.reply_to(message, f"Received photo ID: {photo_id}")

bot.polling()


import random
from telegram import Update, BotCommand
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = '7112867167:AAE7qQdvSLaUIg4A6Qxs46qjw7hNlKkF_U8'
CHANNEL_ID = '@MegaEndless'
MESSAGE_ID = 24574
MESSAGE_IDS = [25621, 25622, 25623, 25624, 25625, 25626, 25627, 25628, 25629, 25630]
KOMARU_MESSAGE_IDS = [25836, 25837, 25838, 25839, 25840, 25841, 25842, 25843, 25844, 25845, 25846, 25847, 25848]

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def caesar_cipher(text: str, shift: int = 3) -> str:
    def shift_char(c: str) -> str:
        if 'а' <= c <= 'я':
            return chr((ord(c) - ord('а') + shift) % 32 + ord('а'))
        elif 'А' <= c <= 'Я':
            return chr((ord(c) - ord('А') + shift) % 32 + ord('А'))
        else:
            return c
    return ''.join(shift_char(c) for c in text)

@dispatcher.add_handler(("chiki"))
def spam_message(update: Update, context: CallbackContext) -> None:
    if context.args:
        word = ' '.join(context.args)
        update.effective_message.reply_text(f'{word}чики')
    else:
        update.effective_message.reply_text('Пожалуйста, укажите слово после команды /chiki.')

def caesar_command(update: Update, context: CallbackContext) -> None:
    if context.args:
        word = ' '.join(context.args)
        encrypted_word = caesar_cipher(word)
        update.effective_message.reply_text(f'Зашифрованное слово: {encrypted_word}')
    else:
        update.effective_message.reply_text('Пожалуйста, укажите слово после команды /caesar.')

def admin_command(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text("Главный администратор: @chayteechaytee")

def anime(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    context.bot.copy_message(chat_id=chat_id, from_chat_id=CHANNEL_ID, message_id=MESSAGE_ID)

def send_random_photo(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    message_id = random.choice(MESSAGE_IDS)
    context.bot.copy_message(chat_id=chat_id, from_chat_id=CHANNEL_ID, message_id=message_id)

def send_random_komaru(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    message_id = random.choice(KOMARU_MESSAGE_IDS)
    context.bot.copy_message(chat_id=chat_id, from_chat_id=CHANNEL_ID, message_id=message_id)

def set_bot_commands(updater: Updater) -> None:
    commands = [
        BotCommand('admin', 'Кто главный админ'),
        BotCommand('chiki', 'Слово с суффиксом "чики"'),
        BotCommand('caesar', 'Шифратор Цезаря'),
        BotCommand('anime', 'Аниме 5 часов'),
        BotCommand('cute', 'Рандомная милота'),
        BotCommand('komaru', 'Рандомная Комару')
    ]
    updater.bot.set_my_commands(commands)

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("chiki", spam_message))
    dispatcher.add_handler(CommandHandler("c", spam_message))
    dispatcher.add_handler(CommandHandler("caesar", caesar_command))
    dispatcher.add_handler(CommandHandler("ca", caesar_command))
    dispatcher.add_handler(CommandHandler("admin", admin_command))
    dispatcher.add_handler(CommandHandler('anime', anime))
    dispatcher.add_handler(CommandHandler('a', anime))
    dispatcher.add_handler(CommandHandler('cute', send_random_photo))
    dispatcher.add_handler(CommandHandler('cu', send_random_photo))

    dispatcher.add_handler(CommandHandler("komaru", send_random_komaru))
    dispatcher.add_handler(CommandHandler("k", send_random_komaru))

    set_bot_commands(updater)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
