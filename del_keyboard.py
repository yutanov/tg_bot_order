#!/usr/bin/env pyt

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, Filters
from steps import cancel_handler
from questionnaire import BANK, OPTIONS, DELIVERY, OTHER_BANK, ORDER
from questionnaire import bank, other_bank, other_delivery
import logging

DEL_DATA = {
    1: "Есть свой штат курьеров",
    2: "Пользуемся курьерскими службами",
    3: "Нет доставки и не планируем",
    4: "Доставка входит в планы",
}

green_check = '\u2705'
grey_check = '\u2714'
TEXT_1 = "Предоставляете услугу доставки?\n"\
"Можно выбрать несколько вариантов:\n"\
"\n"\
"1. Да, есть свой штат курьеров\n"\
"\n"\
"2. Пользуемся курьерскими службами Яндекс / Деливери и др.\n"\
"\n"\
"3. Нет доставки и не планируем\n"\
"\n"\
"4. Доставка входит в планы\n"\
"\n"
CHECK = grey_check
BUTTONS = []
KEYS = {'1': (0, 0), '2': (0, 1), '3': (1, 0), '4': (1, 1)}
BACK = chr(100)

keyboard = [
[
    InlineKeyboardButton(f'1 {CHECK}', callback_data='1'),
    InlineKeyboardButton(f'2 {CHECK}', callback_data='2'),
],
[
    InlineKeyboardButton(f'3 {CHECK}', callback_data='3'),
    InlineKeyboardButton(f'4 {CHECK}', callback_data='4'),
],
[InlineKeyboardButton("Другое", callback_data='other')],
[
    InlineKeyboardButton("\u2b05 Назад", callback_data='back'),
    InlineKeyboardButton('Продолжить \u27A1', callback_data='next'),
    ],
]


def start_delivery(update, context):

    msg = False
    try:
        context.user_data[BANK] = update.callback_query.data
    except:
        context.user_data[BANK] = update.message.text
        msg = True

    global CHECK
    global keyboard
    global BUTTONS
    CHECK = grey_check
    for data in BUTTONS:
        keyboard[KEYS[data][0]][KEYS[data][1]] = InlineKeyboardButton(
            f'{data} {CHECK}', callback_data=f'{data}')
    reply_markup = InlineKeyboardMarkup(keyboard)
    for i in range(1,5):
        context.user_data[f'BUTTON_{i}'] = False
    BUTTONS = []

    if msg:
        update.message.reply_text(text=TEXT_1, reply_markup=reply_markup)
    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(TEXT_1, reply_markup=reply_markup)
    return DELIVERY


def clicked(click=None, data=None):
    global keyboard
    global CHECK
    global BUTTONS
    if click == True:
        CHECK = green_check
    else:
        CHECK = grey_check

    BUTTONS.append(data)
    keyboard[KEYS[data][0]][KEYS[data][1]] = InlineKeyboardButton(
        f'{data} {CHECK}', callback_data=f'{data}')

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


def press(update, context):
    data = update.callback_query.data
    global CLICK

    if context.user_data[f'BUTTON_{data}'] == False:
        context.user_data[f'BUTTON_{data}'] = True
    else:
        context.user_data[f'BUTTON_{data}'] = False
    reply_keyboard = clicked(context.user_data[f'BUTTON_{data}'], data)
    update.callback_query.edit_message_text(text=TEXT_1, reply_markup=reply_keyboard)
    return DELIVERY


def save(update, context):
    text = ''
    for i in range(1, 5):
        text += f'{DEL_DATA[i]} - ' + str(context.user_data[f'BUTTON_{i}']) + '\n'
    context.user_data[DELIVERY] = text
    return OPTIONS


keyboard_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_delivery,
            pattern='^' + 'sber' + '$|^' + 'tinkoff' + '$|^' + 'cp' + '$|^' + 'ukassa' + '$'),
        CallbackQueryHandler(other_bank, pattern='^' + 'other' + '$'),
        MessageHandler(Filters.all, start_delivery, pass_user_data=True),
        ],
    states={
        DELIVERY: [
            CallbackQueryHandler(press,
                pattern='^'+str(1)+'$|^'+str(2)+'$|^'+str(3)+'$|^'+str(4)+'$'),
            CallbackQueryHandler(start_delivery,
                pattern='^' + 'sber' + '$|^' + 'tinkoff' + '$|^' + 'cp' + '$|^' + 'ukassa' + '$'),
            CallbackQueryHandler(other_delivery, pattern='^' + 'other' + '$'),
            CallbackQueryHandler(bank, pattern='^' + 'back' + '$'),
            CallbackQueryHandler(save, pattern='^'+'next'+'$'),
            ],
    },
    map_to_parent={
        OPTIONS: OPTIONS,
    },
    fallbacks=[
        CommandHandler('cancel', cancel_handler),
    ],
    )
