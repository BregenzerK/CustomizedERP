# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kunden', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apfel',
            fields=[
                ('fabrikats_id', models.AutoField(serialize=False, primary_key=True)),
                ('fabrikat', models.CharField(max_length=50)),
                ('verkaufspreis', models.DecimalField(max_digits=8, decimal_places=2)),
                ('lagerbestand', models.IntegerField(default=0)),
                ('artikelnummer', models.IntegerField(max_length=50)),
                ('produktkategorie', models.CharField(max_length=50, choices=[(b'Kunst', b'Kunst'), (b'Handwerk', b'Handwerk')])),
                ('hersteller', models.CharField(max_length=50)),
                ('produktbeschreibung', models.TextField()),
                ('listenpreisVK', models.DecimalField(max_digits=8, decimal_places=2)),
                ('ausmasse', models.CharField(max_length=50)),
                ('farben', models.CharField(max_length=50)),
                ('haltbarkeitsdatum', models.DateField()),
                ('mwst_klasse', models.IntegerField(max_length=50, choices=[(19, b'19 Prozent'), (7, b'7 Prozent')])),
                ('EK', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
                ('durchschn_EK', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
                ('letzter_EK', models.DecimalField(max_digits=8, decimal_places=2)),
                ('bemerkung', models.TextField(blank=True)),
                ('ean_nummer', models.IntegerField(max_length=50)),
                ('meldebestand', models.IntegerField(max_length=5)),
                ('preisart', models.CharField(max_length=50, choices=[(b'Stueck', b'Einzelpreis'), (b'Gewicht', b'Gewichtpreis'), (b'Meter', b'Meterpreis')])),
                ('seriennummer', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faden',
            fields=[
                ('fabrikats_id', models.AutoField(serialize=False, primary_key=True)),
                ('fabrikat', models.CharField(max_length=50)),
                ('verkaufspreis', models.DecimalField(max_digits=8, decimal_places=2)),
                ('lagerbestand', models.IntegerField(default=0)),
                ('artikelnummer', models.IntegerField(max_length=50)),
                ('produktkategorie', models.CharField(max_length=50, choices=[(b'Kunst', b'Kunst'), (b'Handwerk', b'Handwerk')])),
                ('hersteller', models.CharField(max_length=50)),
                ('produktbeschreibung', models.TextField()),
                ('listenpreisVK', models.DecimalField(max_digits=8, decimal_places=2)),
                ('ausmasse', models.CharField(max_length=50)),
                ('farben', models.CharField(max_length=50)),
                ('haltbarkeitsdatum', models.DateField()),
                ('mwst_klasse', models.IntegerField(max_length=50, choices=[(19, b'19 Prozent'), (7, b'7 Prozent')])),
                ('EK', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
                ('durchschn_EK', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
                ('letzter_EK', models.DecimalField(max_digits=8, decimal_places=2)),
                ('bemerkung', models.TextField(blank=True)),
                ('ean_nummer', models.IntegerField(max_length=50)),
                ('meldebestand', models.IntegerField(max_length=5)),
                ('preisart', models.CharField(max_length=50, choices=[(b'Stueck', b'Einzelpreis'), (b'Gewicht', b'Gewichtpreis'), (b'Meter', b'Meterpreis')])),
                ('seriennummer', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inventur',
            fields=[
                ('inventur_id', models.AutoField(serialize=False, primary_key=True)),
                ('datum', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inventurposition',
            fields=[
                ('inventurposition_id', models.AutoField(serialize=False, primary_key=True)),
                ('produkt', models.CharField(max_length=50)),
                ('lagerbestand_real', models.IntegerField(max_length=50)),
                ('gesamtwert', models.DecimalField(editable=False, max_digits=8, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lieferant',
            fields=[
                ('lieferanten_id', models.AutoField(serialize=False, primary_key=True)),
                ('firmenname', models.CharField(max_length=50)),
                ('ansprechpartner', models.CharField(max_length=50)),
                ('strasse', models.CharField(max_length=50)),
                ('plz', models.CharField(max_length=5)),
                ('stadt', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75)),
                ('telefon', models.CharField(max_length=50)),
                ('homepage', models.URLField()),
                ('ust_id', models.CharField(max_length=50)),
                ('konto_id', models.ForeignKey(to='kunden.Konto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inventur',
            name='position',
            field=models.ManyToManyField(to='lager.Inventurposition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faden',
            name='lieferant',
            field=models.ForeignKey(to='lager.Lieferant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apfel',
            name='lieferant',
            field=models.ForeignKey(to='lager.Lieferant'),
            preserve_default=True,
        ),
    ]
