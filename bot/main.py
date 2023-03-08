import json
import telebot
from telebot.types import Message, CallbackQuery

import config, buttons as mk, utils
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

@bot.callback_query_handler(func=lambda call: True)
def call_back_handler(call: CallbackQuery):
    print(call.data)
    jsn = json.loads(call.data)
    data, dtype = jsn["data"], jsn["type"]
    ch_id = call.message.chat.id
    msg_id = call.message.id

    if dtype == "reaction":
        utils.add_or_edit_reaction(ch_id, **data) #data["post_id"], data["smile_id"])
        bot.edit_message_reply_markup(ch_id, msg_id, reply_markup=mk.reaction_markup(data["post_id"]))

if __name__=="__main__":
    bot.infinity_polling(skip_pending=False)