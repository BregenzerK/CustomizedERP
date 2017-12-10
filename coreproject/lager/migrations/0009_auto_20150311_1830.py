# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0008_auto_20150311_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apfel',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 18, 30, 27, 670000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='faden',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 18, 30, 27, 670000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produkt',
            name='lagerbestand',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
