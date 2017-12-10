# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0012_auto_20150316_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instanzen_Lautsprecher',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('seriennummer', models.IntegerField(unique=True)),
                ('verkauft', models.BooleanField(default=False)),
                ('standort', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lautsprecher',
            fields=[
                ('produkt_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='lager.Produkt')),
                ('artikelnummer', models.IntegerField(max_length=50)),
                ('produktkategorie', models.CharField(max_length=50, choices=[(b'Kurzwaren', b'Kurzwaren'), (b'Handwerk', b'Handwerk')])),
                ('hersteller', models.CharField(max_length=50)),
                ('produktbeschreibung', models.TextField()),
                ('listenpreisVK', models.DecimalField(max_digits=8, decimal_places=2)),
                ('mwst_klasse', models.IntegerField(max_length=50, choices=[(19, b'19 Prozent'), (7, b'7 Prozent')])),
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
            model_name='instanzen_nagel',
            name='fabrikat',
        ),
        migrations.DeleteModel(
            name='Instanzen_Nagel',
        ),
        migrations.RemoveField(
            model_name='nagel',
            name='lieferant',
        ),
        migrations.RemoveField(
            model_name='nagel',
            name='produkt_ptr',
        ),
        migrations.DeleteModel(
            name='Nagel',
        ),
        migrations.AddField(
            model_name='instanzen_lautsprecher',
            name='fabrikat',
            field=models.ForeignKey(to='lager.Lautsprecher'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='faden',
            name='EK',
        ),
        migrations.AddField(
            model_name='produkt',
            name='EK',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
    ]
