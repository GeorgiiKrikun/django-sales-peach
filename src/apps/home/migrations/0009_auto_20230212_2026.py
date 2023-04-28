# Generated by Django 3.2.16 on 2023-02-12 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20230211_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextended',
            name='last_activity',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userextended',
            name='requests_today',
            field=models.IntegerField(default=0),
        ),
    ]