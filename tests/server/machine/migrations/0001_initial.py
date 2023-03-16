# -*- coding: utf-8 -*-
# Copyright © 2023 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

# Generated by Django 3.2.18 on 2023-03-16 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('arch', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=32)),
                ('cpu_count', models.SmallIntegerField()),
                ('memory', models.IntegerField(help_text='Memory in gigabytes (GB)')),
                ('created_at', models.DateTimeField()),
                ('powered_on', models.BooleanField()),
                ('os', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='machine.operatingsystem')),
            ],
        ),
    ]
