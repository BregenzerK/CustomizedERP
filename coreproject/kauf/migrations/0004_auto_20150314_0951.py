# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kauf', '0003_auto_20150314_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='warenposition',
            name='available',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='angebot',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 14, 9, 51, 31, 510000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 14, 9, 51, 31, 510000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zahlungkauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 14, 9, 51, 31, 510000)),
            preserve_default=True,
        ),
    ]
