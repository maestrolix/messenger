# Generated by Django 3.2 on 2022-01-28 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0003_thread_last_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagephoto',
            name='image',
            field=models.ImageField(upload_to='thread/messages/2022/01/28', verbose_name='Фотография сообщения'),
        ),
    ]
