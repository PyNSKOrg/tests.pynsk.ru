# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from testapp.models import ResultView

class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0027_resultview'),
    ]

    operations = [
        migrations.RunSQL(ResultView.SQL),
    ]
