from flask import Flask
from flask_caching import Cache
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler, dispatcher, MessageHandler, Filters, ConversationHandler
import logging

from handlers import startUp, echo, animesearch, animekeyboard, button, start, help_command, search


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 60 * 20  # 20 minutes expiry for session ids
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

from controller import *


updater = Updater("1547014681:AAHEqNoxtSz0kpMhKzrVJ_qDH_L5KdDaVhc", use_context=True)
dispatcher = updater.dispatcher

def main():
    # dispatcher.add_handler(CommandHandler('start1', start1))
    # dispatcher.add_handler(CallbackQueryHandler(help1, pattern='help1'))
    # dispatcher.add_handler(CallbackQueryHandler(cancel, pattern='cancel'))
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    #updater = Updater("1547014681:AAHEqNoxtSz0kpMhKzrVJ_qDH_L5KdDaVhc", use_context=True)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('help', help_command))
    search_handler = MessageHandler(Filters.regex(r'search'), search)
    dispatcher.add_handler(search_handler)

    #Tutorial
    search_handler = MessageHandler(Filters.regex(r'search'), search)
    updater.dispatcher.add_handler(search_handler)
    start_handler = CommandHandler('startup', startUp)

    dispatcher.add_handler(start_handler)
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), animesearch)
    # updater.dispatcher.add_handler(echo_handler)

    #animekeyboard
    animekeyboard_handler = CommandHandler('animekeyboard', animekeyboard)
    dispatcher.add_handler(animekeyboard_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    return updater


def start1(update: Update, context: CallbackContext) -> None:
    keyboard = [
                 [InlineKeyboardButton('Help', callback_data='help')]
               ]
    # Create initial message:
    message = 'Welcome.'
    update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

def help1(bot, update):
    keyboard = [
                 [InlineKeyboardButton('Leave', callback_data='cancel')]
               ]
    bot.edit_message_text(
    text='Help ... help..',
    chat_id=update.callback_query.message.chat_id,
    message_id=update.callback_query.message.message_id,
    reply_markup=InlineKeyboardMarkup(keyboard)
    )
    bot.answer_callback_query(update.callback_query.id, text='')

def cancel(bot, update):

    bot.edit_message_text(
    text='Bye',
    chat_id=update.callback_query.message.chat_id,
    message_id=update.callback_query.message.message_id,
    )
    bot.answer_callback_query(update.callback_query.id, text='')

    return ConversationHandler.END

if __name__ == "__main__":
    main()

