from django.conf import settings
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import TeleBot, types
from telebot.types import Update, ReplyKeyboardRemove

from apps.bot.templates.text import success_location
from apps.user.models import Customer

bot_tokens = settings.BOT_TOKENS

avia_customer_bot = TeleBot(bot_tokens['avia_customer'])
auto_customer_bot = TeleBot(bot_tokens['auto_customer'])


class BotWebhook(APIView):
    permission_classes = [AllowAny, ]

    @staticmethod
    def post(request):
        update = Update.de_json(request.data)
        avia_customer_bot.process_new_updates([update])
        auto_customer_bot.process_new_updates([update])
        return Response({'message': 'Success!',
                         'status': status.HTTP_200_OK})


@avia_customer_bot.message_handler(content_types=['location'])
def handle_content_avia(message: types.Message):
    if avia_customer_bot.user.id == message.reply_to_message.from_user.id:
        tg_id = message.chat.id
        customer = get_object_or_404(Customer, tg_id=tg_id)
        location = message.location.to_dict()
        customer.location = location
        customer.save()
        delivery = customer.deliveries.order_by('-id').first()
        avia_customer_bot.send_message(chat_id=tg_id, text=success_location, reply_markup=ReplyKeyboardRemove())
        avia_customer_bot.send_location(chat_id=-1002187675934, reply_to_message_id=delivery.telegram_message_id,
                                        latitude=location['latitude'], longitude=location['longitude'])


@auto_customer_bot.message_handler(content_types=['location'])
def handle_content_auto(message: types.Message):
    if auto_customer_bot.user.id == message.reply_to_message.from_user.id:
        tg_id = message.chat.id
        customer = get_object_or_404(Customer, tg_id=tg_id)
        location = message.location.to_dict()
        customer.location = location
        customer.save()
        delivery = customer.deliveries.order_by('-id').first()
        auto_customer_bot.send_message(chat_id=tg_id, text=success_location, reply_markup=ReplyKeyboardRemove())
        auto_customer_bot.send_location(chat_id=-1002187675934, reply_to_message_id=delivery.telegram_message_id,
                                        latitude=location['latitude'], longitude=location['longitude'])
