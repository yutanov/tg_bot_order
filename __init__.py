#!/usr/bin/env pyt

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, CallbackContext, MessageHandler
from telegram.ext import ConversationHandler
from steps import start_handler, name_handler, cancel_handler, about
from steps import phone_handler, questionnaire
from steps import NAME, CALLBACK_BEGIN, CHOOSE, PHONE, QUESTION
from questionnaire import start_questionnaire, num_of_shops, city, system
from questionnaire import order_at_desk, bank, loyalty
from questionnaire import tips, other_tasks, finish
from questionnaire import other_system, other_bank, other_delivery, other_options
from questionnaire import NAME_OF_PROJECT, NUM_OF_SHOPS, CITY, SYSTEM, ORDER, BANK, OPTIONS
from questionnaire import LOYALTY, TIPS, TASKS, DELIVERY
from del_keyboard import keyboard_conv
from opt_keyboard import keyboard_conv_opt

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, _):
    start_button = "Начать"
    start_text = 'Добрый день ...\n'\
    'Здесь Вы можете оставить ....\n'\
    '\n'\
    'Для старта, нажмите "Начать" \U0001F447'
    keyboard = [
        [
            InlineKeyboardButton(start_button, callback_data=CALLBACK_BEGIN),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(start_text, reply_markup=reply_markup)


def help_command(update, _):
    update.message.reply_text("Используйте `/start` для запуска бота.")


def restart(update, _):
    updater.dispatcher.add_handler(conv_handler)


if __name__ == '__main__':
    updater = Updater("TOKEN")

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_handler, pass_user_data=True),
            CallbackQueryHandler(start_handler, pattern='^' + 'x1' + '$'),
        ],
        states={
            NAME: [
                MessageHandler(Filters.all, name_handler, pass_user_data=True),
            ],
            CHOOSE: [
                CallbackQueryHandler(about, pattern='^' + 'about' + '$'),
                CallbackQueryHandler(phone_handler, pattern='^' + 'app' + '$'),
                CallbackQueryHandler(name_handler, pattern='^' + 'back' + '$')
            ],
            PHONE: [
                MessageHandler(Filters.all, questionnaire, pass_user_data=True),
            ],
            QUESTION: [
                CallbackQueryHandler(start_questionnaire, pattern='^' + 'questions' + '$'),
                CallbackQueryHandler(phone_handler, pattern='^' + 'back' + '$'),
            ],
            NAME_OF_PROJECT: [
                MessageHandler(Filters.all, num_of_shops, pass_user_data=True)
            ],
            NUM_OF_SHOPS: [
                MessageHandler(Filters.all, city, pass_user_data=True)
            ],
            CITY: [
                MessageHandler(Filters.all, system, pass_user_data=True)
            ],
            SYSTEM: [
                CallbackQueryHandler(order_at_desk,
                    pattern='^' + 'iiko' + '$|^' + 'qr' + '$|^' + 'rk' + '$'),
                CallbackQueryHandler(other_system, pattern='^' + 'other' + '$'),
                MessageHandler(Filters.all, order_at_desk, pass_user_data=True),
            ],
            ORDER: [
                CallbackQueryHandler(bank,
                    pattern='^' + 'yes' + '$|^' + 'no' + '$'),
                CallbackQueryHandler(system, pattern='^' + 'back' + '$'),
            ],
            BANK: [
                keyboard_conv,
            ],
            OPTIONS: [
                keyboard_conv_opt,
            ],
            LOYALTY: [
                 MessageHandler(Filters.all, tips, pass_user_data=True),
            ],
            TIPS: [
                CallbackQueryHandler(other_tasks,
                    pattern='^' + 'netmonet' + '$|^' + 'cloudtips' + '$|^' + 'no_tips' + '$'),
            ],
            TASKS: [
                MessageHandler(Filters.all, finish, pass_user_data=True),
                CallbackQueryHandler(start_handler, pattern='^' + 'x1' + '$'),
            ],

        },
        fallbacks=[
            CommandHandler('start', start),
            CommandHandler('help', help_command),
            CommandHandler('cancel', cancel_handler),
        ],
    )

    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('cancel', cancel_handler))

    updater.start_polling()
    updater.idle()
