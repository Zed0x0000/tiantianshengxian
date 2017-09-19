# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consignee', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('postcode', models.CharField(max_length=6)),
                ('phone', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=20)),
                ('user_password', models.CharField(max_length=40)),
                ('user_email', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='deliveryinfo',
            name='user',
            field=models.ForeignKey(to='df_user.UserInfo'),
        ),
    ]
