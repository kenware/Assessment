# Generated by Django 2.1.4 on 2019-01-01 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0006_auto_20190101_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_correct_choice',
            field=models.BooleanField(default=False),
        ),
    ]