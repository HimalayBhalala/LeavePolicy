# Generated by Django 4.2.11 on 2024-11-27 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0016_remove_leaverequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='hr_status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=15),
        ),
    ]
