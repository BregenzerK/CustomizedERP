# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('einkauf', '0005_auto_20150317_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bestellanforderung',
            old_name='menge_banf',
            new_name='menge',
        ),
        migrations.AlterField(
            model_name='bestellung',
            name='lieferdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 17, 15, 38, 3, 321000)),
            preserve_default=True,
        ),
    ]
