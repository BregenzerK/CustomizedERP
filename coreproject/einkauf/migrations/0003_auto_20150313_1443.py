# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('einkauf', '0002_auto_20150313_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bestellposition',
            name='erhalten',
        ),
        migrations.AlterField(
            model_name='bestellung',
            name='lieferdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 13, 14, 43, 0, 815000)),
            preserve_default=True,
        ),
    ]
