# Generated by Django 5.1.2 on 2024-10-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0003_alter_leaverequest_leave_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='requested_date',
            field=models.DateField(),
        ),
    ]
