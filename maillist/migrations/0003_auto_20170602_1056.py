# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-02 15:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("maillist", "0002_auto_20150611_1516")]

    operations = [
        migrations.AlterModelOptions(
            name="mailinglist", options={"base_manager_name": "objects"}
        ),
        migrations.AlterModelOptions(
            name="member", options={"base_manager_name": "objects"}
        ),
    ]
