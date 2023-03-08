from django.db import models
import datetime
from django_celery_beat.models import PeriodicTask, ClockedSchedule


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


class Smile(models.Model):
    char = models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return self.char
    


class Post(models.Model):
    class PostType(models.TextChoices):
        VIDEO = "video"
        PHOTO = "photo"
        TEXT = "text"
        
    type = models.CharField(max_length=5, choices=PostType.choices, default=PostType.PHOTO)
    title = models.CharField(max_length=55, blank=True)
    body = models.TextField()
    media = models.FileField(upload_to="uploads/", blank=True)
    smiles = models.ManyToManyField(Smile)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.media:
            self.type = self.PostType.TEXT
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.title if self.title else self.body[:55]



class Reaction(models.Model):
    smile = models.ForeignKey(Smile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user} - {self.post} - {self.smile}"
    

class Ad(models.Model):
    name = models.CharField(
        max_length=55, unique=True, blank=True, 
        help_text="Short name of your Ad")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        help_text="Slect which post do you want to send to users.")
    active = models.BooleanField(default=True)
    clocked = models.ForeignKey(
        ClockedSchedule, on_delete=models.CASCADE, null=True, blank=True,
        help_text= ("Select time for sending AD."
                    "If you will not set time, AD will be automatically sent after 5 seconds.")
    )
    send_to = models.ManyToManyField(BotUser)
    task_id = models.PositiveIntegerField(editable=False, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.clocked:
            self.clocked = ClockedSchedule.objects.create(
                clocked_time=datetime.datetime.now() + datetime.timedelta(seconds=5)
            )
        
        super().save(*args, **kwargs) # Save for id
        
        if not self.name:
            self.name = f"ad_{self.pk}"
                
        if self.task_id:
            task = PeriodicTask.objects.get(pk=self.task_id)
            task.name = self.name
            task.enabled = self.active
            task.clocked = self.clocked
            task.save()
        else:
            task = PeriodicTask.objects.create(
                name = self.name,
                task = "backend.tasks.send_ad",
                enabled = self.active,
                clocked = self.clocked,
                one_off = True,
                args = f"[{self.id}]",
            )
            self.task_id = task.pk      
        super().save(*args, **kwargs)
          
        
    def delete(self, *args, **kwargs):
        task = PeriodicTask.objects.get(pk=self.task_id)
        print(task)
        task.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name



        