# Generated by Django 4.2.6 on 2023-11-07 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speach', '0005_userdata_last_use_date_userdata_uses_left'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='last_use_date',
        ),
    ]