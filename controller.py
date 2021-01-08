from pprint import pprint

from mal.anime_search import AnimeSearchResult
from ratelimit import limits
import requests

import telebot
from telebot import types

from flask import request, jsonify
from mal import Anime, AnimeSearch
from pip._internal import commands
from telebot.types import Update
from telegram  import InlineKeyboardButton, InlineKeyboardMarkup, update
from telegram.ext import CallbackContext, Updater, CommandHandler


from api.dialogflow_api import detect_intent_via_text, detect_intent_via_event
from api.telegram_api import send_message, bot, send_message_with_options
from beans.session import Session
from beans.user import User
from cache import get_current_session
from command_handlers import COMMAND_HANDLERS, handle_invalid_command
from constants import MAIN_SUGGESTIONS
from handlers import start
from intent_handlers import INTENT_HANDLERS, handle_invalid_intent, __show_main_suggestions
from main import app
from utils import \
    get_user_from_request, \
    get_user_input_from_request, \
    default_if_blank, \
    is_not_blank, \
    get_user_command_from_request

ONE_SECOND = 1


@limits(calls=2, period=ONE_SECOND)
def call_api(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response


@app.route('/')
def hello_world():
    return 'Hello, World!'


# Validates incoming webhook request to make sure required fields are present, before processing
@app.route('/webhook', methods=['POST'])
def webhook():
    updater = Updater("1561103971:AAEr8QvFWgfKVwhDihLrhnO6mr0TnXGc-04", use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    #updater = startUpdater()
    req_body = request.get_json()
    user = get_user_from_request(req_body)
    session = get_current_session(user)
    user_input = get_user_input_from_request(req_body)

    try :
        search = AnimeSearch(user_input).results
        #sendKeyboard(user, updater, search)
        malid = search[0].mal_id
        anime = Anime(malid)
        # bot.send_message(user.id, str(anime.title_english) + ' is rated ' + str(anime.score))
    except ValueError:
        bot.send_message(user.id, 'No anime found')

    return 'Anime is rated '


# Calls Dialogflow API to trigger an intent match
# Calls the corresponding function handler for the intent result action if present
def __process_dialogflow_input(user: User, session: Session, user_input):
    intent_result = detect_intent_via_text(session.id, user_input)
    intent_action = default_if_blank(intent_result.action, '')
    __show_main_suggestions(user, intent_result, session.id)
    return intent_result
