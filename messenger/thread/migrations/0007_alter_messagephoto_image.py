# Generated by Django 3.2 on 2022-01-29 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0006_auto_20220128_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagephoto',
            name='image',
            field=models.ImageField(upload_to='thread/messages/2022/01/29', verbose_name='Фотография сообщения'),
        ),
    ]
