# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='gclick',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gcontent',
            field=tinymce.models.HTMLField(default=b'<h1>\xe8\xbf\x99\xe6\x98\xaf\xe6\x8f\x8f\xe8\xbf\xb0\xe5\xbe\x97\xe6\xb0\xb4\xe6\x9e\x9c</h1>'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gintroduction',
            field=models.CharField(default=b'\xe8\xbf\x99\xe6\x98\xaf\xe6\xb0\xb4\xe6\x9e\x9c', max_length=200),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gprice',
            field=models.DecimalField(default=88, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gstock',
            field=models.IntegerField(default=999),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gtitle',
            field=models.CharField(default=b'\xe6\xb0\xb4\xe6\x9e\x9c', max_length=20),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='type',
            field=models.ForeignKey(default=2, to='df_goods.TypeInfo'),
        ),
    ]
