# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kauf', '0004_auto_20150314_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='angebot',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 19, 59, 5, 664000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 19, 59, 5, 662000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zahlungkauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 19, 59, 5, 667000)),
            preserve_default=True,
        ),
    ]
