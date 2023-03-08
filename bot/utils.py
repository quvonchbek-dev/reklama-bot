from backend.models import Reaction, BotUser, Post, Smile


def count_reaction(post_id, smile_id):
    return Reaction.objects.filter(post__id=post_id).filter(smile__id=smile_id).count()


def add_or_edit_reaction(chat_id, post_id, smile_id):
    reaction = Reaction.objects.filter(user__chat_id=chat_id).filter(post__id=post_id).first()
    smile = Smile.objects.get(pk=smile_id)
    post = Post.objects.get(pk=post_id)
    user = BotUser.objects.get(chat_id=chat_id)
    if reaction:
        if reaction.smile.id == smile_id:
            return reaction.delete()
        reaction.smile = smile
        return reaction.save()
    return Reaction.objects.create(smile=smile, post=post, user=user)

def get_post_reactions(post_id):
    return Post.objects.get(pk=post_id).smiles.all()
