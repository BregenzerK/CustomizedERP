# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kunden', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bestellanforderung',
            fields=[
                ('banf_id', models.AutoField(serialize=False, primary_key=True)),
                ('fabrikat', models.CharField(max_length=50)),
                ('menge', models.IntegerField(max_length=5)),
                ('bestellt', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bestellposition',
            fields=[
                ('position_id', models.AutoField(serialize=False, primary_key=True)),
                ('fabrikat', models.CharField(max_length=50)),
                ('menge', models.IntegerField(max_length=5)),
                ('erhalten', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bestellung',
            fields=[
                ('bestell_id', models.AutoField(serialize=False, primary_key=True)),
                ('summe', models.DecimalField(max_digits=10, decimal_places=2)),
                ('status_offen', models.BooleanField(default=True)),
                ('lieferort', models.CharField(max_length=50)),
                ('lieferdatum', models.DateField(default=datetime.datetime(2015, 3, 13, 14, 40, 45, 309000))),
                ('bestellposition', models.ManyToManyField(to='einkauf.Bestellposition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MitteilungBanf',
            fields=[
                ('mitteilung_id', models.AutoField(serialize=False, primary_key=True)),
                ('nachricht', models.TextField()),
                ('gelesen', models.BooleanField(default=False)),
                ('bestellanforderung', models.ForeignKey(to='einkauf.Bestellanforderung')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ZahlungBestellung',
            fields=[
                ('zahlungs_id', models.AutoField(serialize=False, primary_key=True)),
                ('verwendungszweck', models.TextField()),
                ('datum', models.DateField()),
                ('bestellung', models.ForeignKey(to='einkauf.Bestellung')),
                ('konto', models.ForeignKey(to='kunden.Konto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
