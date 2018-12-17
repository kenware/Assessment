# Generated by Django 2.1.4 on 2018-12-17 14:04

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_choices',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='answer',
            name='created_at',
            field=models.DateField(default=datetime.date(2018, 12, 17)),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='created_at',
            field=models.DateField(default=datetime.date(2018, 12, 17)),
        ),
        migrations.AlterField(
            model_name='question',
            name='created_at',
            field=models.DateField(default=datetime.date(2018, 12, 17)),
        ),
        migrations.AlterField(
            model_name='score',
            name='created_at',
            field=models.DateField(default=datetime.date(2018, 12, 17)),
        ),
    ]
