# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0003_auto_20150311_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apfel',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 13, 4, 59, 742000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='faden',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 13, 4, 59, 742000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instanzen_apfel',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instanzen_faden',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
