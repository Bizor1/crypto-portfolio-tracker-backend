# Generated by Django 3.2.1 on 2023-01-26 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_transactions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='date_created',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 1, 26, 13, 28, 48, 989387)),
        ),
    ]
