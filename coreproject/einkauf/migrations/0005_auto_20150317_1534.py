# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('einkauf', '0004_auto_20150313_1443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bestellanforderung',
            old_name='menge',
            new_name='menge_banf',
        ),
        migrations.AlterField(
            model_name='bestellung',
            name='lieferdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 17, 15, 34, 38, 209000)),
            preserve_default=True,
        ),
    ]
