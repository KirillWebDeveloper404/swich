# Generated by Django 4.0.2 on 2022-02-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0005_remove_kategory_for_who_kategory_for_who'),
    ]

    operations = [
        migrations.CreateModel(
            name='ADS_db',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='name')),
                ('phone', models.TextField(verbose_name='phone')),
                ('address', models.TextField(verbose_name='address')),
                ('link', models.TextField(verbose_name='link')),
                ('desc', models.TextField(verbose_name='desc')),
            ],
            options={
                'verbose_name': 'ADS',
                'verbose_name_plural': 'ADSs',
                'db_table': 'ads',
                'managed': True,
            },
        ),
    ]
