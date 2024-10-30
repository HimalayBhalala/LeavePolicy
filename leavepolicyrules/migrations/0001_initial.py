# Generated by Django 5.1.2 on 2024-10-29 08:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField()),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('hr', 'Hr'), ('pm', 'Pm'), ('tl', 'Tl'), ('developer', 'Developer')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'leaverule',
                'verbose_name_plural': 'leaverules',
                'db_table': 'leaverule',
            },
        ),
        migrations.CreateModel(
            name='LeaveType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'leavetype',
                'verbose_name_plural': 'leavetypes',
                'db_table': 'leavetype',
            },
        ),
        migrations.CreateModel(
            name='LeaveReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leavepolicyrules.leavetype')),
            ],
            options={
                'verbose_name': 'leavereason',
                'verbose_name_plural': 'leavereasons',
                'db_table': 'leavereason',
            },
        ),
    ]