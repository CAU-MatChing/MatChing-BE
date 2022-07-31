# Generated by Django 4.0.6 on 2022-07-31 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matzips', '0002_alter_matzip_name'),
        ('profiles', '0001_initial'),
        ('matchings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matching',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profiles.profile'),
        ),
        migrations.AlterField(
            model_name='matching',
            name='matzip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='matzips.matzip'),
        ),
    ]
