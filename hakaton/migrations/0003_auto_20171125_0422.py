# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 04:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hakaton', '0002_auto_20171125_0420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('plan_data', models.CharField(max_length=15000)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='likes',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AddField(
            model_name='plan',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hakaton.Customer'),
        ),
    ]
