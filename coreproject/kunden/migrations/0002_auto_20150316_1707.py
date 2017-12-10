# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kunden', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='konto',
            name='blz',
        ),
        migrations.RemoveField(
            model_name='konto',
            name='iban',
        ),
        migrations.AddField(
            model_name='konto',
            name='BLZ',
            field=models.PositiveIntegerField(default=1234569, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='konto',
            name='IBAN',
            field=models.PositiveIntegerField(default=9874562, max_length=34),
            preserve_default=False,
        ),
    ]
