from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import utils
import json

def reaction_markup(post_id):
    btn = []
    smiles = utils.get_post_reactions(post_id)
    for smile in smiles:
        data = {
            "type": "reaction",
            "data": {"post_id": post_id, "smile_id": smile.id}
        }
        btn.append(
            InlineKeyboardButton(
                text=f"{smile.char} {utils.count_reaction(post_id, smile.id) or ' '}",
                callback_data=str(data).replace("'", '"')
            )
        )
    kb = InlineKeyboardMarkup()
    kb.add(*btn)
    return kb
