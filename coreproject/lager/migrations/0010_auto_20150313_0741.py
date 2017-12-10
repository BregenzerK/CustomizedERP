# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0009_auto_20150311_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apfel',
            name='haltbarkeitsdatum',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='haltbarkeitsdatum',
        ),
        migrations.AddField(
            model_name='apfel',
            name='mindestbestellwert',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faden',
            name='mindestbestellwert',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instanzen_apfel',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 13, 7, 41, 57, 62000)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instanzen_faden',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 13, 7, 41, 57, 62000)),
            preserve_default=True,
        ),
    ]
