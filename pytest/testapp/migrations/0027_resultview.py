# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0026_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultView',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('test_name', models.CharField(max_length=200, verbose_name=b'Test name')),
                ('number_of_questions', models.PositiveIntegerField()),
                ('number_of_right_answers', models.PositiveIntegerField()),
            ],
            options={
                'managed': False,
            },
        ),
    ]
