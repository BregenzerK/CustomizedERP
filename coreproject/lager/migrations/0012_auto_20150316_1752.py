# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0011_auto_20150313_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instanzen_Nagel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('seriennummer', models.IntegerField(unique=True)),
                ('verkauft', models.BooleanField(default=False)),
                ('standort', models.CharField(max_length=50)),
                ('haltbarkeitsdatum', models.DateField(default=datetime.datetime(2015, 3, 16, 17, 52, 27, 1000))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nagel',
            fields=[
                ('produkt_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='lager.Produkt')),
                ('artikelnummer', models.IntegerField(max_length=50)),
                ('produktkategorie', models.CharField(max_length=50, choices=[(b'Kurzwaren', b'Kurzwaren'), (b'Handwerk', b'Handwerk')])),
                ('hersteller', models.CharField(max_length=50)),
                ('produktbeschreibung', models.TextField()),
                ('listenpreisVK', models.DecimalField(max_digits=8, decimal_places=2)),
                ('mwst_klasse', models.IntegerField(max_length=50, choices=[(19, b'19 Prozent'), (7, b'7 Prozent')])),
                ('EK', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
                ('durchschn_EK', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
                ('letzter_EK', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
                ('bemerkung', models.TextField(blank=True)),
                ('meldebestand', models.IntegerField(max_length=5)),
                ('lieferant', models.ForeignKey(to='lager.Lieferant')),
            ],
            options={
            },
            bases=('lager.produkt',),
        ),
        migrations.RemoveField(
            model_name='apfel',
            name='lieferant',
        ),
        migrations.RemoveField(
            model_name='apfel',
            name='produkt_ptr',
        ),
        migrations.RemoveField(
            model_name='instanzen_apfel',
            name='fabrikat',
        ),
        migrations.DeleteModel(
            name='Apfel',
        ),
        migrations.DeleteModel(
            name='Instanzen_Apfel',
        ),
        migrations.AddField(
            model_name='instanzen_nagel',
            name='fabrikat',
            field=models.ForeignKey(to='lager.Nagel'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='faden',
            name='ausmasse',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='ean_nummer',
        ),
        migrations.RemoveField(
            model_name='instanzen_faden',
            name='haltbarkeitsdatum',
        ),
        migrations.AlterField(
            model_name='faden',
            name='produktkategorie',
            field=models.CharField(max_length=50, choices=[(b'Kurzwaren', b'Kurzwaren'), (b'Handwerk', b'Handwerk')]),
            preserve_default=True,
        ),
    ]
