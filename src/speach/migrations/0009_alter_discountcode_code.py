# Generated by Django 4.2.6 on 2023-11-22 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speach', '0008_discountcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='code',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
