# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0021_auto_20160111_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.ForeignKey(related_name='raitings', to='testapp.Player')),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='interval',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Retake interval in seconds'),
        ),
        migrations.AddField(
            model_name='rating',
            name='test',
            field=models.ForeignKey(to='testapp.Test'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('test', 'player')]),
        ),
    ]
