# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produkttyp',
            name='EK',
        ),
        migrations.RemoveField(
            model_name='produkttyp',
            name='aktionspreis',
        ),
        migrations.RemoveField(
            model_name='produkttyp',
            name='bilder',
        ),
        migrations.RemoveField(
            model_name='produkttyp',
            name='haltbarkeitsdatum',
        ),
    ]
