# Generated by Django 2.2.16 on 2021-12-13 12:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20211213_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 13, 12, 9, 38, 379479, tzinfo=utc)),
        ),
    ]
