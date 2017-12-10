# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produkt',
            fields=[
                ('fabrikats_id', models.AutoField(serialize=False, primary_key=True)),
                ('fabrikat', models.CharField(max_length=50)),
                ('verkaufspreis', models.DecimalField(max_digits=8, decimal_places=2)),
                ('lagerbestand', models.IntegerField(default=0)),
                ('preisart', models.CharField(max_length=50, choices=[(b'Stueck', b'Einzelpreis'), (b'Gewicht', b'Gewichtpreis'), (b'Meter', b'Meterpreis')])),
                ('seriennummer', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='apfel',
            name='fabrikat',
        ),
        migrations.RemoveField(
            model_name='apfel',
            name='fabrikats_id',
        ),
        migrations.RemoveField(
            model_name='apfel',
            name='lagerbestand',
        ),
        migrations.RemoveField(
            model_name='apfel',
            name='preisart',
        ),
        migrations.RemoveField(
            model_name='apfel',
            name='seriennummer',
        ),
        migrations.RemoveField(
            model_name='apfel',
            name='verkaufspreis',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='fabrikat',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='fabrikats_id',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='lagerbestand',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='preisart',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='seriennummer',
        ),
        migrations.RemoveField(
            model_name='faden',
            name='verkaufspreis',
        ),
        migrations.AddField(
            model_name='apfel',
            name='produkt_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='lager.Produkt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faden',
            name='produkt_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='lager.Produkt'),
            preserve_default=False,
        ),
    ]
