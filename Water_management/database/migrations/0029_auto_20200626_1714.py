# Generated by Django 3.0.7 on 2020-06-26 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0028_auto_20200626_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='desc',
            field=models.TextField(null=True),
        ),
    ]
