# Generated by Django 3.2 on 2022-01-27 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='message',
            table='message',
        ),
        migrations.AlterModelTable(
            name='thread',
            table='thread',
        ),
    ]