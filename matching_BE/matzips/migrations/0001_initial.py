# Generated by Django 4.0.6 on 2022-09-09 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matzip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60, null=True, unique=True)),
                ('waiting', models.IntegerField(default=0)),
                ('matched', models.IntegerField(default=0)),
            ],
        ),
    ]
