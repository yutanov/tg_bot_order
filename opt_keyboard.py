#!/usr/bin/env pyt

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, Filters
from steps import cancel_handler
from questionnaire import OPTIONS, DELIVERY, LOYALTY
from questionnaire import other_options
import logging

OPT_DATA = {
    1: "Оформить доставку",
    2: "Оформить самовывоз / предзаказ",
    3: "Заказать за стол",
    4: "Сделать онлайн-бронь стола",
    5: "Использовать программу лояльности",
}
green_check = '\u2705'
grey_check = '\u2714'
TEXT = "Какую возможность хотите дать своим клиентам в Тг?\n"\
"Можно выбрать все варианты\n"\
"\n"\
"1. Оформить доставку\n"\
"\n"\
"2. Оформить самовывоз / предзаказ\n"\
"\n"\
"3. Заказать за стол\n"\
"\n"\
"4. Сделать онлайн-бронь стола\n"\
"\n"\
"5. Использовать программу лояльности\n"\
"\n"
CHECK = grey_check
CLICK = False
BUTTONS = []
KEYS = {'1': (0, 0), '2': (0, 1), '3': (1, 0), '4': (1, 1), '5': (2, 0)}

keyboard_opt = [
    [
        InlineKeyboardButton(f'1 {CHECK}', callback_data='1'),
        InlineKeyboardButton(f'2 {CHECK}', callback_data='2'),
    ],
    [
        InlineKeyboardButton(f'3 {CHECK}', callback_data='3'),
        InlineKeyboardButton(f'4 {CHECK}', callback_data='4'),
    ],
    [
        InlineKeyboardButton(f'5 {CHECK}', callback_data='5'),
        InlineKeyboardButton("Другое", callback_data='other'),
    ],
    [
        InlineKeyboardButton('Продолжить \u27A1', callback_data='next'),
    ],
]


def start_options(update, context):
    msg = False
    try:
        update.callback_query.data
    except:
        context.user_data[DELIVERY] = context.message.text
        msg = True
    print('opt_keyboard')
    global CHECK
    global keyboard_opt
    global BUTTONS
    CHECK = grey_check
    for data in BUTTONS:
        keyboard_opt[KEYS[data][0]][KEYS[data][1]] = InlineKeyboardButton(
            f'{data} {CHECK}', callback_data=f'{data}')
    reply_keyboard = InlineKeyboardMarkup(keyboard_opt)
    for i in range(1,6):
        context.user_data[f'BUTTON_{i}'] = False
    BUTTONS = []
    if msg:
        contex.message.reply_text(text=TEXT, reply_markup=reply_keyboard)
    else:
        update.callback_query.edit_message_text(text=TEXT, reply_markup=reply_keyboard)
    return OPTIONS


def clicked(click=None, data=None):
    global keyboard
    global CHECK
    global BUTTONS
    if click == True:
        CHECK = green_check
    else:
        CHECK = grey_check

    BUTTONS.append(data)
    keyboard_opt[KEYS[data][0]][KEYS[data][1]] = InlineKeyboardButton(
        f'{data} {CHECK}', callback_data=f'{data}')

    reply_markup = InlineKeyboardMarkup(keyboard_opt)

    return reply_markup


def press(update, context):
    data = update.callback_query.data
    global CLICK
    if context.user_data[f'BUTTON_{data}'] == False:
        context.user_data[f'BUTTON_{data}'] = True
    else:
        context.user_data[f'BUTTON_{data}'] = False

    reply_keyboard = clicked(context.user_data[f'BUTTON_{data}'], data)
    update.callback_query.edit_message_text(text=TEXT, reply_markup=reply_keyboard)
    return OPTIONS


def save(update, context):
    text = ''
    for i in range(1, 6):
        text += f'{OPT_DATA[i]} - ' + str(context.user_data[f'BUTTON_{i}']) + '\n'
    context.user_data[OPTIONS] = text
    print('save OPTIONS')
    print(context.user_data[DELIVERY])
    print(update.callback_query.data)
    return LOYALTY


keyboard_conv_opt = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_options, pattern='^' + 'next' + '$'),
        CallbackQueryHandler(other_options, pattern='^' + 'other' + '$'),
        MessageHandler(Filters.all, start_options, pass_user_data=True),
        ],
    states={
        OPTIONS: [
            CallbackQueryHandler(press,
                pattern='^'+str(1)+'$|^'+str(2)+'$|^'+str(3)+'$|^'+str(4)+'$|^'+str(5)+'$'),
            CallbackQueryHandler(other_options, pattern='^' + 'other' + '$'),
            CallbackQueryHandler(save, pattern='^'+'next'+'$'),
            MessageHandler(Filters.all, start_options, pass_user_data=True)
            ],
    },
        map_to_parent={
            LOYALTY: LOYALTY,
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )
