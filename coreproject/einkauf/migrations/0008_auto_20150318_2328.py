# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('einkauf', '0007_auto_20150318_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mitteilungbanf',
            name='bestellanforderung',
        ),
        migrations.DeleteModel(
            name='MitteilungBanf',
        ),
        migrations.AlterField(
            model_name='bestellung',
            name='lieferdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 23, 28, 34, 734000)),
            preserve_default=True,
        ),
    ]
