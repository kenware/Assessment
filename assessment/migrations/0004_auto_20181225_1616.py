# Generated by Django 2.1.4 on 2018-12-25 16:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0003_score_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created_at',
            field=models.DateField(default=datetime.date(2018, 12, 25)),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='created_at',
            field=models.DateField(default=datetime.date(2018, 12, 25)),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='created_at',
            field=models.DateField(default=datetime.date(2018, 12, 25)),
        ),
        migrations.AlterField(
            model_name='score',
            name='created_at',
            field=models.DateField(default=datetime.date(2018, 12, 25)),
        ),
    ]