# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Konto',
            fields=[
                ('konto_id', models.AutoField(serialize=False, primary_key=True)),
                ('iban', models.IntegerField(max_length=34)),
                ('kontoinhaber', models.CharField(max_length=50)),
                ('blz', models.IntegerField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kunde',
            fields=[
                ('kunden_id', models.AutoField(serialize=False, primary_key=True)),
                ('nachname', models.CharField(max_length=50)),
                ('vorname', models.CharField(max_length=50)),
                ('titel', models.CharField(max_length=50, blank=True)),
                ('telefonnummer', models.CharField(max_length=50)),
                ('organisation', models.CharField(max_length=50, blank=True)),
                ('strasse', models.CharField(max_length=50)),
                ('plz', models.CharField(max_length=50)),
                ('stadt', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75)),
                ('kundengruppe', models.CharField(max_length=50, choices=[(b'Kate 3', b'Kate 3'), (b'Kate 5', b'Kate 5')])),
                ('privatkunde', models.BooleanField(default=True)),
                ('kreditwuerdig', models.BooleanField(default=False)),
                ('konto_id', models.ForeignKey(to='kunden.Konto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
