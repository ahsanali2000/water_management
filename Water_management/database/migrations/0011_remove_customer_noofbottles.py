# Generated by Django 3.0.2 on 2020-06-23 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_customer_notinarea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='NoOfBottles',
        ),
    ]