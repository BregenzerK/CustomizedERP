# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('einkauf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bestellung',
            name='lieferdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 13, 14, 41, 42, 617000)),
            preserve_default=True,
        ),
    ]
