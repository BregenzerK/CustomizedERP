# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0013_auto_20150316_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faden',
            name='produktkategorie',
            field=models.CharField(max_length=50, choices=[(b'Kurzwaren', b'Kurzwaren'), (b'Elektronik', b'Elektronik')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventurposition',
            name='gesamtwert',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lautsprecher',
            name='produktkategorie',
            field=models.CharField(max_length=50, choices=[(b'Kurzwaren', b'Kurzwaren'), (b'Elektronik', b'Elektronik')]),
            preserve_default=True,
        ),
    ]
