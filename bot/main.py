import telebot
from telebot.types import Message, CallbackQuery

import config
from backend.models import BotUser


bot = telebot.TeleBot(
    token=config.TOKEN,
    parse_mode="HTML",
)

@bot.message_handler(["start"])
def start_message(message: Message):
    chat = message.chat
    new_user = BotUser.objects.get_or_create(
        chat_id=chat.id,
        first_name=chat.first_name,
        last_name=chat.last_name,
        username=chat.username,
    )
    if new_user[1]:
        bot.send_message(chat.id, f"Salom, {chat.first_name}.\n\nBotga xush kelibsiz!")
    else:
        bot.send_message(chat.id, "Yana bir bor ko'rib turganimdan xursandman.")
        
if __name__=="__main__":
    bot.infinity_polling(skip_pending=False)