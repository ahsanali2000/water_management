# Generated by Django 3.0.2 on 2020-06-14 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
