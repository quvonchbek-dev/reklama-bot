from django.db import models
from django_quill.fields import QuillField
import datetime
from multiselectfield import MultiSelectField

class BotUser(models.Model):
    class Lang(models.TextChoices):
        UZ = 'uz'
        RU = 'ru'
        EN = 'en'

    first_name = models.CharField(max_length=255, verbose_name='Ism')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Familiya')
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.CharField(unique=True, max_length=255)
    
    lang = models.CharField(max_length=2, choices=Lang.choices, default=Lang.UZ)
    created = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name or ''])

    def __str__(self):
        return self.get_full_name()

    # class Meta:
    #     verbose_name = 'Foydalanuvchi'
    #     verbose_name_plural = 'Foydalanuvchilar'
      
class Post(models.Model):
    class PostType(models.TextChoices):
        VIDEO = "video"
        PHOTO = "photo"
        TEXT = "text"
        
    type = models.CharField(max_length=5, choices=PostType.choices, default=PostType.PHOTO)
    title = models.CharField(max_length=55, blank=True)
    body = QuillField()
    media = models.FileField(upload_to="uploads/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.media:
            self.type = self.PostType.TEXT
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.title if self.title else self.body[:55]

class Ad(models.Model):
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    title = models.CharField(max_length=55, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ad_post")
    time = models.TimeField(default=datetime.time(8, 30))
    days = MultiSelectField(verbose_name="Weekdays", choices=DAYS_OF_WEEK, max_length=255)
    repeat = models.BooleanField(default=True)
    send_to = models.ManyToManyField(BotUser)
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"ad_{self.id}"
        super().save(*args, **kwargs)
        