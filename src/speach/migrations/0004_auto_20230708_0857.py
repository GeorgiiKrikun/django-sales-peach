# Generated by Django 3.2.16 on 2023-07-08 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('speach', '0003_auto_20230708_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='pastrequest',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='speach.service'),
        ),
        migrations.AlterField(
            model_name='pastrequest',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='speach.company'),
        ),
    ]
