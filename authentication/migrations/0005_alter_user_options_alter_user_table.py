# Generated by Django 5.1.2 on 2024-10-29 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]