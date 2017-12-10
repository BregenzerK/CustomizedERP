# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0010_auto_20150313_0741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apfel',
            name='mindestbestellwert',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='mindestbestellwert',
        ),
        migrations.AddField(
            model_name='lieferant',
            name='mindestbestellwert',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instanzen_apfel',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 13, 7, 45, 10, 774000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instanzen_faden',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 13, 7, 45, 10, 774000)),
            preserve_default=True,
        ),
    ]
