#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging

from mal import Anime
from mal.anime_search import AnimeSearchResult
from telebot import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from api.telegram_api import send_message, bot
from beans.user import User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# def sendKeyboard(user: User, queries) -> None:
#     queryCount = len(queries)
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
#     for x in range(queryCount):
#         malid = queries[x].mal_id
#         anime = Anime(malid)
#         markup.add(str(anime.title_english))
#         if x > 6:
#             break
#
#     bot.send_message(user.id, 'choose one', reply_markup=markup)
#     #print(update.callback_query)

def sendkeyboard(update: Update, user: User, queries) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Anime", callback_data='1'),
            InlineKeyboardButton("Manga", callback_data='2'),
        ],
        [InlineKeyboardButton("Web Comics", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    anime = Anime(int(query.data))
    query.edit_message_text(text=f"{anime.title} is rated: {anime.score}")
    #query.edit_message_text(text=f"Selected option: {query.data}")


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")


def startUpdater():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1547014681:AAHEqNoxtSz0kpMhKzrVJ_qDH_L5KdDaVhc", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    return updater
