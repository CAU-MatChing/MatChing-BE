# Generated by Django 4.0.6 on 2022-09-02 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matzips', '0002_alter_matzip_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matzip',
            name='location',
        ),
    ]