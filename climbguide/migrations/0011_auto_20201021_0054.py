# Generated by Django 3.1.2 on 2020-10-21 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climbguide', '0010_auto_20201021_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointofinterest',
            name='latitude',
            field=models.FloatField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='pointofinterest',
            name='longitude',
            field=models.FloatField(blank=True, default=None),
        ),
    ]