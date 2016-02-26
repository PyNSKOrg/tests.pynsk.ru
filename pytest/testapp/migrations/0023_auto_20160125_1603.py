# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0022_auto_20160125_0938'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='rating',
            name='player',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='test',
        ),
        migrations.AlterField(
            model_name='game',
            name='test',
            field=models.ForeignKey(related_name='games', to='testapp.Test'),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
