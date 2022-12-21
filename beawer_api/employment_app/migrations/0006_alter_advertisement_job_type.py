# Generated by Django 4.1.4 on 2022-12-21 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment_app', '0005_advertisement_description_advertisement_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='job_type',
            field=models.CharField(choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Intern', 'Intern'), ('Remote', 'Remote'), ('Hybrid', 'Hybrid')], default='Full Time', max_length=50),
        ),
    ]