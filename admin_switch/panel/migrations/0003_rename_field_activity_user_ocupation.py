# Generated by Django 4.0.2 on 2022-02-22 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_alter_user_options_rename_length_user_lenght'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='field_activity',
            new_name='ocupation',
        ),
    ]
