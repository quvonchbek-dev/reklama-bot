# Generated by Django 4.1.7 on 2023-03-06 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='name',
            field=models.CharField(help_text='Short name of your Ad', max_length=55, unique=True),
        ),
    ]