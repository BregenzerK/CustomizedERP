# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kunden', '0001_initial'),
        ('lager', '0007_auto_20150311_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Angebot',
            fields=[
                ('angebot_id', models.AutoField(serialize=False, primary_key=True)),
                ('summe', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('mehrwertsteuer', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('rabatt', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('rabattarten', models.CharField(blank=True, max_length=50, choices=[(b'prozentrabatt', b'%'), (b'betragsrabatt', b'EUR')])),
                ('rabattgrund', models.TextField(blank=True)),
                ('standort', models.CharField(max_length=50)),
                ('datum', models.DateField(default=datetime.datetime(2015, 3, 11, 14, 35, 20, 449000))),
                ('kunde', models.ForeignKey(to='kunden.Kunde')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kauf',
            fields=[
                ('kauf_id', models.AutoField(serialize=False, primary_key=True)),
                ('summe', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('mehrwertsteuer', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('rabatt', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('rabattarten', models.CharField(blank=True, max_length=50, choices=[(b'prozentrabatt', b'%'), (b'betragsrabatt', b'EUR')])),
                ('rabattgrund', models.TextField(blank=True)),
                ('standort', models.CharField(max_length=50)),
                ('datum', models.DateField(default=datetime.datetime(2015, 3, 11, 14, 35, 20, 449000))),
                ('kunde', models.ForeignKey(to='kunden.Kunde')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MitteilungKauf',
            fields=[
                ('mitteilung_id', models.AutoField(serialize=False, primary_key=True)),
                ('nachricht', models.TextField()),
                ('gelesen', models.BooleanField(default=False)),
                ('kauf', models.ForeignKey(to='kauf.Kauf')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Warenposition',
            fields=[
                ('position_id', models.AutoField(serialize=False, primary_key=True)),
                ('menge', models.IntegerField(max_length=5)),
                ('fabrikat', models.ForeignKey(to='lager.Produkt')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ZahlungKauf',
            fields=[
                ('zahlungs_id', models.AutoField(serialize=False, primary_key=True)),
                ('verwendungszweck', models.TextField()),
                ('datum', models.DateField(default=datetime.datetime(2015, 3, 11, 14, 35, 20, 449000))),
                ('zahlart', models.CharField(max_length=20, choices=[(b'Raten', b'Ratenzahlung'), (b'Kreditkarte', b'Kreditkarte')])),
                ('kauf', models.ForeignKey(to='kauf.Kauf')),
                ('konto', models.ForeignKey(to='kunden.Konto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='kauf',
            name='warenposition',
            field=models.ManyToManyField(to='kauf.Warenposition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='angebot',
            name='warenposition',
            field=models.ManyToManyField(to='kauf.Warenposition'),
            preserve_default=True,
        ),
    ]
