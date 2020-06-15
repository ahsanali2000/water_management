# Generated by Django 3.0.7 on 2020-06-14 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0015_auto_20200614_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Area'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]