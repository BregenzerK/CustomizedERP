# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0002_auto_20150308_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instanzen_Apfel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seriennummer', models.IntegerField(unique=True)),
                ('verkauft', models.BooleanField(default=False)),
                ('standort', models.CharField(max_length=50)),
                ('fabrikat', models.ForeignKey(to='lager.Apfel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instanzen_Faden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seriennummer', models.IntegerField(unique=True)),
                ('verkauft', models.BooleanField(default=False)),
                ('standort', models.CharField(max_length=50)),
                ('fabrikat', models.ForeignKey(to='lager.Faden')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='apfel',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 12, 54, 1, 46000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apfel',
            name='letzter_EK',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='faden',
            name='haltbarkeitsdatum',
            field=models.DateField(default=datetime.datetime(2015, 3, 11, 12, 54, 1, 46000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='faden',
            name='letzter_EK',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produkt',
            name='fabrikat',
            field=models.CharField(unique=True, max_length=50),
            preserve_default=True,
        ),
    ]
