from mal import AnimeSearch, Anime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def startUp(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def animesearch(update, context):
    try :
        search = AnimeSearch(update.message.text).results
        malid = search[0].mal_id
        anime = Anime(malid)
        #context.bot.send_message(chat_id=update.effective_chat.id, text=str(anime.title_english) + ' is rated ' + str(anime.score))
        keyboard = [
        [InlineKeyboardButton(str(Anime(search[0].mal_id).title_english), callback_data=str(search[0].mal_id))],
        [InlineKeyboardButton(str(Anime(search[1].mal_id).title_english), callback_data=str(search[1].mal_id)),],
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
