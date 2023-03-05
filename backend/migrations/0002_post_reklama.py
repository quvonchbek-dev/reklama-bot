# Generated by Django 4.1.7 on 2023-03-05 09:59

from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('video', 'Video'), ('photo', 'Photo'), ('text', 'Text')], default='photo', max_length=5)),
                ('title', models.CharField(blank=True, max_length=55)),
                ('body', django_quill.fields.QuillField()),
                ('media', models.FileField(blank=True, upload_to='uploads/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reklama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_time', models.DateTimeField(blank=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reklama_post', to='backend.post')),
                ('send_to', models.ManyToManyField(to='backend.botuser')),
            ],
        ),
    ]