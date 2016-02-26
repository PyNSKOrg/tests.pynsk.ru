# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0024_auto_20160207_0341'),
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
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
