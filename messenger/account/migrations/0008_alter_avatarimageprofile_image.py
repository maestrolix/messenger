# Generated by Django 3.2 on 2022-01-31 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_advuser_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatarimageprofile',
            name='image',
            field=models.ImageField(upload_to='images/account/avatars/2022/01/31', verbose_name='Фотография пользователя'),
        ),
    ]
