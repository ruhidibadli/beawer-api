# Generated by Django 4.1.4 on 2022-12-19 04:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('salary', models.IntegerField()),
                ('job_type', models.CharField(choices=[('FULL TIME', 'FULL TIME'), ('PART TIME', 'PART TIME'), ('INTERN', 'INTERN'), ('SEASONAL', 'SEASONAL'), ('CONTRACT', 'CONTRACT')], max_length=50)),
                ('country', models.CharField(max_length=255)),
                ('enabled', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.category')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.employer')),
            ],
        ),
        migrations.CreateModel(
            name='AppliedJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Viewed', 'Viewed'), ('Interview Phase', 'Interview Phase'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=25)),
                ('enabled', models.BooleanField(default=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.applicant')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employment_app.advertisement')),
            ],
        ),
    ]
