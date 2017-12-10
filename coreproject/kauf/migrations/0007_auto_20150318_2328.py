# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kauf', '0006_auto_20150318_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='angebot',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 23, 28, 53, 881000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 23, 28, 53, 881000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zahlungkauf',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 3, 18, 23, 28, 53, 881000)),
            preserve_default=True,
        ),
    ]
