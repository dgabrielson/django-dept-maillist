# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-02 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("maillist", "0003_auto_20170602_1056")]

    operations = [
        migrations.AlterField(
            model_name="mailinglist",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="creation time"),
        ),
        migrations.AlterField(
            model_name="mailinglist",
            name="modified",
            field=models.DateTimeField(
                auto_now=True, verbose_name="last modification time"
            ),
        ),
        migrations.AlterField(
            model_name="mailinglist",
            name="slug",
            field=models.SlugField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name="member",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="creation time"),
        ),
        migrations.AlterField(
            model_name="member",
            name="modified",
            field=models.DateTimeField(
                auto_now=True, verbose_name="last modification time"
            ),
        ),
    ]
