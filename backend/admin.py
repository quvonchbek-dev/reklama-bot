from django.contrib import admin
from .models import BotUser, Ad, Post


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BotUser._meta.fields if field.name != "id"]

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Ad._meta.fields if field.name != "id"]
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "id", "type"]
    list_filter = ["type", "title"]