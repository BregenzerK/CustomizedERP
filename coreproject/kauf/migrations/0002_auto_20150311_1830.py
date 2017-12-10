# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kauf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='angebot',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 18, 30, 46, 242000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 18, 30, 46, 242000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='warenposition',
            name='fabrikat',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zahlungkauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 18, 30, 46, 242000)),
            preserve_default=True,
        ),
    ]
