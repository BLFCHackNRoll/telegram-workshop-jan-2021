from pprint import pprint

from mal.anime_search import AnimeSearchResult
from ratelimit import limits

import requests

import telebot
from telebot import types
from flask import request
from mal import Anime, AnimeSearch
from pip._internal import commands
import telegram

from api.dialogflow_api import detect_intent_via_text, detect_intent_via_event
from api.telegram_api import send_message, bot
from beans.session import Session
from beans.user import User
from cache import get_current_session
from command_handlers import COMMAND_HANDLERS, handle_invalid_command
from intent_handlers import INTENT_HANDLERS, handle_invalid_intent
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
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # FILL IN CODE
#     req_body = request.get_json()
#     user = get_user_from_request(req_body)
#     session = get_current_session(user)
#     user_input = get_user_input_from_request(req_body)
#
#     if is_not_blank(user.id, user_input):
#         __process_dialogflow_input(user, session, user_input)
#     return 'Got your message'

# Validates incoming webhook request to make sure required fields are present, before processing
@app.route('/webhook', methods=['POST'])
def webhook():
    req_body = request.get_json()
    user = get_user_from_request(req_body)
    session = get_current_session(user)
    user_input = get_user_input_from_request(req_body)
    anime = Anime(1)  # Cowboy Bebop
    search = AnimeSearch(user_input).results
    malid = search[0].mal_id
    message = Anime(malid)  # Cowboy Bebop
    message.reload()  # reload object


    handle_option(user.id, message)
    return 'Anime is rated '


def handle_option(id, message):
    menu_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    button1 = types.KeyboardButton(text="image")
    button2 = types.KeyboardButton(text="synopsis")
    button3 = types.KeyboardButton(text="episodes")
    menu_markup.add(button1, button2, button3)
    bot.send_message(id, 'Select one', reply_markup=menu_markup)
    # bot.send_message(id, 'Got it', reply_markup=types.ReplyKeyboardRemove())
    # if user_input == 'image':
    #    bot.send_photo(id, res.url, caption=str(res.title_english) + ' is rated ' + str(res.score))
    return ''


# Here's a simple handler when user presses button with "Button 1" text
@bot.message_handler(content_types=["text"], func=lambda message: message.text == "image")
def func1(message):
    keyboard = types.InlineKeyboardMarkup()
    url_btn = types.InlineKeyboardButton(url="https://stackoverflow.com", text="Go to StackOverflow")
    keyboard.add(url_btn)
    bot.send_message(message.chat.id, "Image handler", reply_markup=keyboard)


# Calls Dialogflow API to trigger an intent match
# Calls the corresponding function handler for the intent result action if present
def __process_dialogflow_input(user: User, session: Session, user_input):
    intent_result = detect_intent_via_text(session.id, user_input)
    intent_action = default_if_blank(intent_result.action, '')
    if is_not_blank(intent_action):
        INTENT_HANDLERS.get(intent_action, handle_invalid_intent)(user, intent_result, session.id)
    return intent_result
