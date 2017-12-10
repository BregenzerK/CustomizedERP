# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0006_auto_20150311_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apfel',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 14, 35, 20, 434000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='faden',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 14, 35, 20, 449000)),
            preserve_default=True,
        ),
    ]
