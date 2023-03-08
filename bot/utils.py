from backend.models import Reaction, BotUser, Post, Smile


def get_bot_user(chat_id):
    return BotUser.objects.get(chat_id=chat_id)


def count_reaction(post_id, smile_id):
    return Reaction.objects.filter(post__id=post_id).filter(smile__id=smile_id).count()


def get_reaction(chat_id, post_id):
    return Reaction.objects.filter(user__chat_id=chat_id).filter(post__id=post_id).first()


def remove_reaction(chat_id, post_id):
    reaction = get_reaction(chat_id, post_id)
    if reaction:
        return reaction.delete()
    return False


def add_or_edit_reaction(chat_id, post_id, smile_id):
    reaction = get_reaction(chat_id, post_id)
    smile = Smile.objects.get(pk=smile_id)
    post = Post.objects.get(pk=post_id)
    if reaction:
        if reaction.smile.id == smile_id:
            return reaction.delete()
        reaction.smile = smile
        return reaction.save()
    return Reaction.objects.create(smile=smile, post=post, user=get_bot_user(chat_id))

def get_post_reactions(post_id):
    return Post.objects.get(pk=post_id).smiles.all()
