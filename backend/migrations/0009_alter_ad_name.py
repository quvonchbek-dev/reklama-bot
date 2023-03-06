# Generated by Django 4.1.7 on 2023-03-06 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_ad_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='name',
            field=models.CharField(blank=True, help_text='Short name of your Ad', max_length=55, unique=True),
        ),
    ]
