# Generated by Django 2.1.4 on 2018-12-17 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0002_auto_20181217_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='status',
            field=models.CharField(blank=True, default='not started', max_length=250),
        ),
    ]