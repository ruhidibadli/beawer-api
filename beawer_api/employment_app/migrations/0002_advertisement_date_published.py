# Generated by Django 4.1.4 on 2022-12-20 05:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employment_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='date_published',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
