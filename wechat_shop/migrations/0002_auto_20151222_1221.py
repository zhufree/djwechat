# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='price',
        ),
        migrations.AddField(
            model_name='good',
            name='discount',
            field=models.DecimalField(default=0.85, max_digits=2, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='good',
            name='final_price',
            field=models.DecimalField(default=0.0, max_digits=4, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='good',
            name='raw_price',
            field=models.DecimalField(default=0.0, max_digits=4, decimal_places=3),
            preserve_default=True,
        ),
    ]
