# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kauf', '0005_auto_20150318_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mitteilungkauf',
            name='kauf',
        ),
        migrations.DeleteModel(
            name='MitteilungKauf',
        ),
        migrations.AlterField(
            model_name='angebot',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 23, 28, 3, 237000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 23, 28, 3, 237000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zahlungkauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 23, 28, 3, 237000)),
            preserve_default=True,
        ),
    ]
