# Generated by Django 5.1.2 on 2024-10-29 08:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leavepolicyrules', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_leave', models.CharField(blank=True, max_length=200, null=True)),
                ('leave_description', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_by', to=settings.AUTH_USER_MODEL)),
                ('leave_reason', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leavepolicyrules.leavereason')),
                ('leave_rule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leavepolicyrules.leaverule')),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leavepolicyrules.leavetype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'leaverequest',
                'verbose_name_plural': 'leaverequests',
                'db_table': 'leaverequest',
            },
        ),
    ]
