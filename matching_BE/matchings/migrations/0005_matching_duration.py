# Generated by Django 4.0.6 on 2022-08-07 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchings', '0004_remove_matching_date_alter_matching_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='matching',
            name='duration',
            field=models.IntegerField(default=1),
        ),
    ]