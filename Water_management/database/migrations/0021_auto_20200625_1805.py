# Generated by Django 3.0.7 on 2020-06-25 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_auto_20200624_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='orders',
            field=models.ManyToManyField(to='database.Order'),
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Area', unique=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Schedule')),
            ],
        ),
    ]
