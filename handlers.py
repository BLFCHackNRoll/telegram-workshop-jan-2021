import random

from mal import AnimeSearch, Anime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

import genre
from genre import action, sports, sliceoflife, horror


def startUp(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def animesearch(update, context):
    try:
        search = AnimeSearch(update.message.text).results
        malid = search[0].mal_id
        anime = Anime(malid)
        # context.bot.send_message(chat_id=update.effective_chat.id, text=str(anime.title_english) + ' is rated ' + str(anime.score))
        keyboard = [
            [InlineKeyboardButton(str(Anime(search[0].mal_id).title_english), callback_data=str(search[0].mal_id))],
            [InlineKeyboardButton(str(Anime(search[1].mal_id).title_english), callback_data=str(search[1].mal_id)), ],
            [InlineKeyboardButton(str(Anime(search[2].mal_id).title_english), callback_data=str(search[2].mal_id))],
            [InlineKeyboardButton(str(Anime(search[3].mal_id).title_english), callback_data=str(search[3].mal_id))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No anime found')

    keyboard = [
        [
            InlineKeyboardButton("Anime", callback_data='1'),
            InlineKeyboardButton("Manga", callback_data='2'),
        ],
        [InlineKeyboardButton("Web Comics", callback_data='3')],
    ]


def animekeyboard(update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Anime", callback_data='1'),
            InlineKeyboardButton("Manga", callback_data='2'),
        ],
        [InlineKeyboardButton("Web Comics", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data == 'searchanime':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Use the keyword search followed by the anime name')
    elif query.data == 'getrecommendations' or query.data == 'donotlike' :
        query.edit_message_text(text='Which genre do you like?', reply_markup=animegenres())
        # context.bot.send_message(chat_id=update.effective_chat.id, text='You should watch Naruto')
    elif 'genre' in query.data:
        slicedgenre = query.data.replace('genre', '').lower()
        value = random.choice(list(eval(slicedgenre).values()))
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(value))
    else:
        anime = Anime(int(query.data))
        query.edit_message_text(text=f"{anime.title} is rated: {anime.score}")
        # query.edit_message_text(text=f"Selected option: {query.data}")


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Search Anime", callback_data='searchanime'),
            InlineKeyboardButton("Recommend Anime", callback_data='getrecommendations'),
        ],
        [InlineKeyboardButton("Web Comics", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('What would you like like to do?', reply_markup=reply_markup)


def search(update: Update, context: CallbackContext) -> None:
    try:
        search = AnimeSearch(update.message.text.replace('search', '')).results
        malid = search[0].mal_id
        anime = Anime(malid)
        # context.bot.send_message(chat_id=update.effective_chat.id, text=str(anime.title_english) + ' is rated ' + str(anime.score))
        keyboard = [
            [InlineKeyboardButton(str(Anime(search[0].mal_id).title_english), callback_data=str(search[0].mal_id))],
            [InlineKeyboardButton(str(Anime(search[1].mal_id).title_english), callback_data=str(search[1].mal_id)), ],
            [InlineKeyboardButton(str(Anime(search[2].mal_id).title_english), callback_data=str(search[2].mal_id))],
            [InlineKeyboardButton(str(Anime(search[3].mal_id).title_english), callback_data=str(search[3].mal_id))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No anime found')

    keyboard = [
        [
            InlineKeyboardButton("Anime", callback_data='1'),
            InlineKeyboardButton("Manga", callback_data='2'),
        ],
        [InlineKeyboardButton("Web Comics", callback_data='3')],
    ]


def animegenres():
    randos = random.sample(genres, 5)
    keyboard = [
        [InlineKeyboardButton(str(randos[0]), callback_data='genre' + str(randos[0]))],
        [InlineKeyboardButton(str(randos[1]), callback_data='genre' + str(randos[1]))],
        [InlineKeyboardButton(str(randos[2]), callback_data='genre' + str(randos[2]))],
        [InlineKeyboardButton(str(randos[3]), callback_data='genre' + str(randos[3]))],
        [InlineKeyboardButton("I don't like these", callback_data="donotlike")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


genres = ["Action"
    , 'Adventure'
    , 'Comedy'
    , 'Drama'
    , 'SliceofLife'
    , 'Fantasy'
    , 'Magic'
    , 'Supernatural'
    , 'Horror'
    , 'Mystery'
    , 'Psychological'
    , 'Romance'
    , 'Sci-Fi'
    , 'Sports']


