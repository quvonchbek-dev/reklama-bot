# Generated by Django 4.1.7 on 2023-03-06 22:01

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_ad_active_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_quill.fields.QuillField(),
        ),
    ]