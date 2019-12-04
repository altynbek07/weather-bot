from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from weather import get_forecasts
from os import getenv

token = getenv('TELEGRAM_TOKEN')

updater = Updater(token, use_context=True)

dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def option(update, context):
    button = [
        [
            InlineKeyboardButton('Option 1', callback_data='1'),
            InlineKeyboardButton('Option 2', callback_data='2')
        ],
        [
            InlineKeyboardButton('Option 3', callback_data='3'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(button)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Choose option', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))


def get_location(update, context):
    button = [
        [
            KeyboardButton('Share Location', request_location=True),
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(button)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Share Location', reply_markup=reply_markup)


def location(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    forecasts = get_forecasts(lat, lon)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=forecasts, reply_markup=ReplyKeyboardRemove())


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

option_handler = CommandHandler('option', option)
dispatcher.add_handler(option_handler)

button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)

get_location_handler = CommandHandler('location', get_location)
dispatcher.add_handler(get_location_handler)

location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)

updater.start_polling()
