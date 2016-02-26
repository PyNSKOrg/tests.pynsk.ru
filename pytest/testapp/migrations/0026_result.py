# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0025_auto_20160221_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('score', models.PositiveSmallIntegerField()),
            ],
            options={
                'managed': False,
            },
        ),
    ]
