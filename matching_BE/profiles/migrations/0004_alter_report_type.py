# Generated by Django 4.0.6 on 2022-09-02 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.CharField(default='', max_length=31),
        ),
    ]
