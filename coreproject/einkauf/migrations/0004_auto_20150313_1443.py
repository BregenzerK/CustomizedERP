# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('einkauf', '0003_auto_20150313_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='bestellposition',
            name='erhalten',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bestellung',
            name='lieferdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 13, 14, 43, 17, 514000)),
            preserve_default=True,
        ),
    ]
