# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('einkauf', '0009_auto_20150318_2328'),
        ('kauf', '0007_auto_20150318_2328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mitteilung',
            fields=[
                ('mitteilung_id', models.AutoField(serialize=False, primary_key=True)),
                ('nachricht', models.TextField()),
                ('gelesen', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MitteilungBanf',
            fields=[
                ('mitteilung_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mitteilungen.Mitteilung')),
                ('bestellanforderung', models.ForeignKey(to='einkauf.Bestellanforderung')),
            ],
            options={
            },
            bases=('mitteilungen.mitteilung',),
        ),
        migrations.CreateModel(
            name='MitteilungKauf',
            fields=[
                ('mitteilung_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mitteilungen.Mitteilung')),
                ('kauf', models.ForeignKey(to='kauf.Kauf')),
            ],
            options={
            },
            bases=('mitteilungen.mitteilung',),
        ),
    ]
