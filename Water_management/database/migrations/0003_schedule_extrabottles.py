# Generated by Django 3.0.7 on 2020-07-01 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_bottles'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='extraBottles',
            field=models.IntegerField(default=0),
        ),
    ]
