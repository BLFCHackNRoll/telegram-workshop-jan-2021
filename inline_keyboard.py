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
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

from api.telegram_api import send_message, bot
from beans.user import User
from handlers import animesearch

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


def echo(update, context, args):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)







