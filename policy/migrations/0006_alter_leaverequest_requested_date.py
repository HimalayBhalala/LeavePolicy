# Generated by Django 4.2.11 on 2024-11-25 03:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0005_alter_leaverequest_requested_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='requested_date',
            field=models.DateField(default=datetime.date(2024, 11, 25)),
        ),
    ]