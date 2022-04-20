#!/usr/bin/env python

import phonenumbers
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

CALLBACK_BEGIN = 'x1'
NAME, CHOOSE, PHONE, QUESTION = range(4)


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


def check_phone(number):
    try:
        number = phonenumbers.parse(number, "RU")
        int_number = phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        if len(int_number) < 10:
            return False
        return int_number
    except:
        return False


def start_handler(update: Update, context: CallbackContext):
    text_hello = "\U0001F5E3 Как мы можем к Вам обращаться?\n"\
        "\n"\
        "Отправьте имя сообщением в любом формате..."
    init = update.callback_query.data
    chat_id = update.callback_query.message.chat.id

    if init != CALLBACK_BEGIN:
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text='/help',
        )
        return ConversationHandler.END

    update.callback_query.answer()
    update.callback_query.bot.send_message(
        chat_id=chat_id,
        text=text_hello
    )
    return NAME


def name_handler(update: Update, context: CallbackContext):
    try:
        context.user_data[NAME] = update.message.text
    except:
        update.callback_query.data
    text = 'Заявка на бота'
    inline_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Оставить заявку', callback_data='app')],
            [InlineKeyboardButton('О нас', callback_data='about')]
        ],
    )
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('logo.jpg', 'rb'),
                           caption=text, reply_markup=inline_buttons,
                           )
    return CHOOSE


def phone_handler(update: Update, context: CallbackContext):
    text = "Укажите номер телефона для связи \U0001f4de"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return PHONE


def questionnaire(update: Update, context: CallbackContext):
    phone = update.message.text
    context.user_data[PHONE] = check_phone(phone)
    if context.user_data[PHONE]:
        with open('file_db.txt', 'a') as f:
            f.write(f"{context.user_data[NAME]} - {context.user_data[PHONE]}\n")

        text = "Благодарим, мы скоро с вами свяжемся! "\
            "\n"\
            "Хотите первый месяц обсуживания бесплатно? "\
            "\n"\
            "Если да, то просим заполнить анкету из 10 вопросов "\
            "для ресторанной сферы и мы соберем для вас "\
            "индивидуальное коммерческое предложение "

        reply_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton('Заполнить анкету', callback_data='questions')],
                [InlineKeyboardButton('\u2b05 Назад', callback_data='back')],
            ]
        )
        update.message.reply_text(text=text, reply_markup=reply_keyboard)
        return QUESTION
    else:
        text = "Укажите, пожалуйста, правильный номер телефона с кодом города "
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return PHONE


def cancel_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Отмена. Для перезапуска бота нажмите /start')
    return ConversationHandler.END


def about(update: Update, context: CallbackContext):
    update.callback_query.answer()
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('\U0001f4ad Быстрая связь', callback_data='app')],
            [InlineKeyboardButton('\u2b05 Назад', callback_data='back')]
        ],
    )
    text = "Наш продукт помогает выстраивать коммуникацию "\
        "и автоматизирует процессы без лишних усилий. "\
        "Скачивать дополнительный софт и создавать приложения "\
        "больше не нужно."\
        "\n\n"\
        "\u2022 Телефон"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('logo.jpg', 'rb'),
                           caption=text, reply_markup=reply_keyboard,
                           )
    return CHOOSE
