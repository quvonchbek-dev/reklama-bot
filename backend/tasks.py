from __future__ import absolute_import, unicode_literals
from datetime import datetime
from celery import shared_task
from telebot import TeleBot
from environs import Env
from core.celery import app
from django.core.exceptions import ObjectDoesNotExist
from backend.models import Ad, BotUser


env = Env()
env.read_env()
TOKEN = env.str("TOKEN")

@app.task
def send_message_test():
    bot = TeleBot(TOKEN, parse_mode="HTML")
    bot.send_message("1183161840", str(datetime.now()))
    return "success"


@shared_task
def send_ad(ad_id):
    try:
        bot = TeleBot(TOKEN, parse_mode="HTML")
        
        def send_msg(msg_type, ch_id, text, media):
            if msg_type=="photo":
                bot.send_photo(ch_id, photo=media, caption=text)
            elif msg_type=="video":
                bot.send_video(ch_id, media, caption=text)
            else:
                bot.send_message(ch_id, text)
                
        ad = Ad.objects.get(pk=ad_id)
        post = ad.post
        users = ad.send_to.all()
        for user in users:
            send_msg(post.type, user.chat_id, post.body, post.media)
        
        # for chat_id in ADMINS:
        #     bot.send_message(chat_id, f"Success!\n\nAd with name {ad.name} sent to users.")
    except ObjectDoesNotExist:
        pass
    return "SUCCESS"
