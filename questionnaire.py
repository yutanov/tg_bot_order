#!/usr/bin/env python

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler
from steps import NAME, PHONE, USER_ID

NAME_OF_PROJECT, NUM_OF_SHOPS, CITY = map(chr, range(4, 7))
SYSTEM, ORDER, BANK, OPTIONS = map(chr, range(7, 11))
LOYALTY, TIPS, TASKS = map(chr, range(11, 14))
DELIVERY, OTHER_BANK, OTHER_SYSTEM = map(chr, range(14, 17))
OTHER_DELIVERY, OTHER_OPTIONS = map(chr, range(17, 19))


OPT_DATA = {
    1: "Оформить доставку",
    2: "Оформить самовывоз / предзаказ",
    3: "Заказать за стол",
    4: "Сделать онлайн-бронь стола",
    5: "Использовать программу лояльности",
}


def start_questionnaire(update: Update, context: CallbackContext):
    text = 'Для формирования КП нам потребуется '\
        "общая информация о вашей компании и пожеланиях "\
        "по функционалу."\
        "\n"\
        "Анкета состоит из 10 коротких вопросов."\
        "И первый из них:"\
        "\n"\
        "Как называется ваш проект?"
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    return NAME_OF_PROJECT


def num_of_shops(update: Update, context: CallbackContext):
    msg = False
    try:
        context.user_data[NAME_OF_PROJECT] = update.message.text
        msg = True
    except:
        update.callback_query.data
    text = "Напишите количество заведений"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    if msg:
        update.message.reply_text(text=text, reply_markup=reply_keyboard)
    else:
        update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return NUM_OF_SHOPS


def city(update: Update, context: CallbackContext):
    msg = False
    try:
        context.user_data[NUM_OF_SHOPS] = update.message.text
        msg = True
    except:
        update.callback_query.data
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    text = "В каком городе или городах находится заведение?"
    if msg:
        if context.user_data[NUM_OF_SHOPS].isdigit():
            update.message.reply_text(text=text, reply_markup=reply_keyboard)
            return CITY
        else:
            other_text = "Укажите, пожалуйста, количество цифрами"
            update.message.reply_text(text=other_text, reply_markup=reply_keyboard)
            return NUM_OF_SHOPS
    else:
        update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
        return CITY


def system(update: Update, context: CallbackContext):
    msg = False
    try:
        context.user_data[CITY] = update.message.text
        msg = True
    except:
        update.callback_query.data
    text = "Какой системой автоматизации для ресторана пользуетесь?"\
        "\n"\
        "Выберите один из пунктов или укажите свой вариант."
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('IIKO', callback_data='iiko')],
            [InlineKeyboardButton('Quik Restro', callback_data='qr')],
            [InlineKeyboardButton('R Keeper', callback_data='rk')],
            [InlineKeyboardButton('Другое', callback_data='other')],
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    if msg:
        update.message.reply_text(text=text, reply_markup=reply_keyboard)
    else:
        update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return SYSTEM


def order_at_desk(update: Update, context: CallbackContext):
    msg = False
    try:
        context.user_data[SYSTEM] = update.callback_query.data
    except:
        context.user_data[SYSTEM] = update.message.text
        msg = True
    text = "Хотите получать заказ сразу на кассу?"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Да", callback_data='yes'),
                InlineKeyboardButton("Нет", callback_data='no'),
            ],
            [InlineKeyboardButton("\u2b05 Назад", callback_data='back')],
        ]
    )
    if msg:
        update.message.reply_text(text=text, reply_markup=reply_keyboard)
    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return ORDER


def bank(update: Update, context: CallbackContext):
    context.user_data[ORDER] = update.callback_query.data
    text = "Укажите наименование банка онлайн-эквайринга"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Сбер', callback_data='sber')],
            [InlineKeyboardButton('Тинькофф', callback_data='tinkoff')],
            [InlineKeyboardButton('Cloud Payments', callback_data='cp')],
            [InlineKeyboardButton('ЮКасса', callback_data='ukassa')],
            [InlineKeyboardButton('Другой', callback_data='other')],
            [InlineKeyboardButton("\u2b05 Назад", callback_data='back')],
        ],
    )
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return BANK


def loyalty(update: Update, context: CallbackContext):
    data_text = ''
    for i in range(1, 6):
        data_text += f'{OPT_DATA[i]} - ' + str(context.user_data[f'BUTTON_{i}']) + '\n'
    context.user_data[OPTIONS] = data_text
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    text = "Используете программу лояльности?"\
        "\n"\
        "Если да, то внешнюю или свою?\n"\
        "Напишите, пожалуйста, название"
    try:
        update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    except:
        update.message.reply_text(text=text, reply_markup=reply_keyboard)
    return LOYALTY


def tips(update: Update, context: CallbackContext):
    msg = False
    try:
        context.user_data[LOYALTY] = update.message.text
        msg = True
    except:
        update.callback_query.data
    text = "Пользуетесь внешними услугами онлайн-чаевых?"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('НетМонет', callback_data='netmonet')],
            [InlineKeyboardButton('CloudTips', callback_data='cloudtips')],
            [InlineKeyboardButton('Не пользуемся', callback_data='no_tips')],
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    if msg:
        update.message.reply_text(text=text, reply_markup=reply_keyboard)
    else:
        update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return TIPS


def other_tasks(update: Update, context: CallbackContext):
    context.user_data[TIPS] = update.callback_query.data
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    text = "И последний!"\
        "\n"\
        "Есть ли дополнительные задачи, которые вы хотели бы автоматизировать?"
    update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return TASKS


def finish(update: Update, context: CallbackContext):
    context.user_data[TASKS] = update.message.text

    text = f'Имя - {context.user_data[NAME]} \n'\
        f'Телефон - {context.user_data[PHONE]} \n'\
        f'Проект - {context.user_data[NAME_OF_PROJECT]} \n'\
        f'Количество - {context.user_data[NUM_OF_SHOPS]} \n'\
        f'Город - {context.user_data[CITY]} \n'\
        f'Сист. авт. - {context.user_data[SYSTEM]} \n'\
        f'Заказ на кассу - {context.user_data[ORDER]} \n'\
        f'Банк - {context.user_data[BANK]} \n'\
        f'Доставка - {context.user_data[DELIVERY]} \n'\
        f'Доп. опции - {context.user_data[OPTIONS]} \n'\
        f'Лояльность - {context.user_data[LOYALTY]} \n'\
        f'Чаевые - {context.user_data[TIPS]} \n'\
        f'Доп. задачи - {context.user_data[TASKS]} \n'\
        "\n"
    with open('questionnaire_db.txt', 'a') as f:
        f.write(text)

    fileID = 'questionnaire_db.txt'
    context.bot.send_document(
        chat_id=USER_ID,
        caption=f"Новая анкета {context.user_data[NAME]} {context.user_data[PHONE]}",
        document=open(fileID, 'rb'),
        filename=fileID,
    )
    text = f"Супер, {context.user_data[NAME]}!\n"\
        "Благодарим за пройденный путь\n"\
        "\n"\
        "Мы вам дарим первый месяц обслуживания\n"\
        "\n"\
        "Мы ушли формировать КП и в ближайшее время с вами свяжемся"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Главное меню \u27A1', callback_data='x1')],
        ],
    )
    update.message.reply_text(text=text, reply_markup=reply_keyboard)
    return ConversationHandler.END


def other_system(update: Update, context: CallbackContext):
    text = "Напишите какой системой автоматизации для ресторана вы пользуетесь"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return OTHER_SYSTEM


def other_bank(update: Update, context: CallbackContext):
    text = "Напишите наименование банка онлайн-эквайринга"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return OTHER_BANK


def other_delivery(update: Update, context: CallbackContext):
    text = "Предоставляете услугу доставки?"\
        "\n"\
        "Напишите свой вариант ответа:"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    try:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    except:
        update.message.reply_text(text=text, reply_markup=reply_keyboard)
    return OTHER_DELIVERY


def other_options(update: Update, context: CallbackContext):
    text = "Какую возможность хотите дать своим клиентам в Тг?"\
        "\n"\
        "Напишите свой вариант ответа:"
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
        ],
    )
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=reply_keyboard)
    return OTHER_OPTIONS
