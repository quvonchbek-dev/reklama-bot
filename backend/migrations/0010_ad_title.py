# Generated by Django 4.1.7 on 2023-03-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_ad_repeat'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='title',
            field=models.CharField(blank=True, max_length=55),
        ),
    ]
