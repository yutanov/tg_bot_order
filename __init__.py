#!/usr/bin/env pyt

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, CallbackContext, MessageHandler
from telegram.ext import ConversationHandler
from steps import start, help_command, start_handler, name_handler, cancel_handler, about
from steps import phone_handler, questionnaire
from steps import NAME, CALLBACK_BEGIN, CHOOSE, PHONE, QUESTION
from questionnaire import start_questionnaire, num_of_shops, city, system
from questionnaire import order_at_desk, bank, loyalty
from questionnaire import tips, other_tasks, finish
from questionnaire import other_system, other_bank, other_delivery, other_options
from questionnaire import NAME_OF_PROJECT, NUM_OF_SHOPS, CITY, SYSTEM, ORDER, BANK, OPTIONS, OTHER_DELIVERY
from questionnaire import LOYALTY, TIPS, TASKS, DELIVERY, OTHER_SYSTEM, OTHER_BANK, OTHER_OPTIONS
from del_keyboard import start_delivery, press
from opt_keyboard import start_options, opt_press

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    updater = Updater("TOKEN")

    conv_handler = ConversationHandler(
        entry_points=[
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
                MessageHandler(Filters.all, city, pass_user_data=True),
                CallbackQueryHandler(start_questionnaire, pattern='^' + 'back' + '$'),
            ],
            CITY: [
                MessageHandler(Filters.all, system, pass_user_data=True),
                CallbackQueryHandler(num_of_shops, pattern='^' + 'back' + '$'),
            ],
            SYSTEM: [
                CallbackQueryHandler(order_at_desk,
                                     pattern='^' + 'iiko' + '$|^' + 'qr' + '$|^' + 'rk' + '$'),
                CallbackQueryHandler(other_system, pattern='^' + 'other' + '$'),
                CallbackQueryHandler(city, pattern='^' + 'back' + '$'),
            ],
            OTHER_SYSTEM: [
                CallbackQueryHandler(system, pattern='^' + 'back' + '$'),
                MessageHandler(Filters.all, order_at_desk, pass_user_data=True),
            ],
            ORDER: [
                CallbackQueryHandler(bank,
                                     pattern='^' + 'yes' + '$|^' + 'no' + '$'),
                CallbackQueryHandler(system, pattern='^' + 'back' + '$'),
            ],
            BANK: [
                CallbackQueryHandler(start_delivery,
                                     pattern='^' + 'sber' + '$|^' + 'tinkoff' + '$|^' + 'cp' + '$|^' + 'ukassa' + '$'),
                CallbackQueryHandler(other_bank, pattern='^' + 'other' + '$'),
                CallbackQueryHandler(order_at_desk, pattern='^' + 'back' + '$'),
            ],
            OTHER_BANK: [
                MessageHandler(Filters.all, start_delivery, pass_user_data=True),
                CallbackQueryHandler(bank, pattern='^' + 'back' + '$'),
            ],
            DELIVERY: [
                CallbackQueryHandler(press,
                                     pattern='^'+str(1)+'$|^'+str(2)+'$|^'+str(3)+'$|^'+str(4)+'$'),
                CallbackQueryHandler(other_delivery, pattern='^' + 'other' + '$'),
                CallbackQueryHandler(bank, pattern='^' + 'back' + '$'),
                CallbackQueryHandler(start_options, pattern='^'+'next'+'$'),
            ],
            OTHER_DELIVERY: [
                MessageHandler(Filters.all, start_options, pass_user_data=True),
                CallbackQueryHandler(start_delivery, pattern='^' + 'back' + '$'),
            ],
            OPTIONS: [
                CallbackQueryHandler(opt_press,
                                     pattern='^'+str(1)+'$|^'+str(2)+'$|^'+str(3)+'$|^'+str(4)+'$|^'+str(5)+'$'),
                CallbackQueryHandler(other_options, pattern='^' + 'other' + '$'),
                CallbackQueryHandler(loyalty, pattern='^'+'next'+'$'),
                CallbackQueryHandler(start_delivery, pattern='^' + 'back' + '$'),
            ],
            OTHER_OPTIONS: [
                MessageHandler(Filters.all, loyalty, pass_user_data=True),
                CallbackQueryHandler(start_options, pattern='^' + 'back' + '$'),
            ],
            LOYALTY: [
                MessageHandler(Filters.all, tips, pass_user_data=True),
                CallbackQueryHandler(start_options, pattern='^' + 'back' + '$'),
            ],
            TIPS: [
                CallbackQueryHandler(other_tasks,
                                     pattern='^' + 'netmonet' + '$|^' + 'cloudtips' + '$|^' + 'no_tips' + '$'),
                CallbackQueryHandler(loyalty, pattern='^' + 'back' + '$'),
            ],
            TASKS: [
                MessageHandler(Filters.all, finish, pass_user_data=True),
                CallbackQueryHandler(tips, pattern='^' + 'back' + '$'),
            ],

        },
        allow_reentry=True,
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
