# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='dt_modified',
            field=models.DateTimeField(null=True, verbose_name=b'date/time of last modification'),
        ),
    ]
