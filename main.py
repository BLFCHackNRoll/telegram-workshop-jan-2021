from flask import Flask
from flask_caching import Cache
from telegram.ext import CallbackQueryHandler, dispatcher, MessageHandler, Filters
import logging

from handlers import startUp, echo, animesearch, animekeyboard

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

from inline_keyboard import button, help_command

config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 60 * 20  # 20 minutes expiry for session ids
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

from controller import *

updater = Updater("1547014681:AAHEqNoxtSz0kpMhKzrVJ_qDH_L5KdDaVhc", use_context=True)
def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    #updater = Updater("1547014681:AAHEqNoxtSz0kpMhKzrVJ_qDH_L5KdDaVhc", use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    #Tutorial
    start_handler = CommandHandler('startup', startUp)
    updater.dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), animesearch)
    updater.dispatcher.add_handler(echo_handler)
    #animekeyboard
    animekeyboard_handler = CommandHandler('animekeyboard', animekeyboard)
    updater.dispatcher.add_handler(animekeyboard_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    return updater


if __name__ == "__main__":
    main()

