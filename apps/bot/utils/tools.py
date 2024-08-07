import logging
from os.path import join as join_path

from django.conf import settings
from telebot import types

logger = logging.getLogger()


def send_instruction(message, bot, caption, file_name, keyboard, loader_text):
    if type(message) is not str:
        message = message.chat.id
    file_path = join_path(settings.MEDIA_ROOT, 'instructions', file_name)
    with open(file_path, 'rb') as video:
        loader = bot.send_message(chat_id=message, text=loader_text,
                                  reply_markup=types.ReplyKeyboardRemove())
        try:
            bot.send_document(chat_id=message, document=video, caption=caption, reply_markup=keyboard)
        except Exception as exc:
            logger.debug(f'Error occurred: {exc.args}')
    bot.delete_message(chat_id=message, message_id=loader.message_id)
