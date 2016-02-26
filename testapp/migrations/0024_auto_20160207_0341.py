# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0023_auto_20160125_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.PositiveSmallIntegerField()),
                ('player', models.ForeignKey(to='testapp.Player')),
                ('test', models.ForeignKey(to='testapp.Test')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('test', 'player')]),
        ),
    ]
