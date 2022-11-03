# Generated by Django 4.0.7 on 2022-08-24 16:29

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orc_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('service_id', models.IntegerField()),
                ('service_name', models.CharField(max_length=100)),
                ('branch_id', models.IntegerField()),
                ('branch_name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
            ],
        ),
        migrations.CreateModel(
            name='SMTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.CharField(max_length=50)),
                ('port', models.IntegerField()),
                ('mail', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=70)),
                ('subject', models.CharField(max_length=150)),
                ('signature', models.TextField()),
                ('to', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=70), blank=True, null=True, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orc_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mkridit.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orc_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mkridit.branch')),
            ],
        ),
        migrations.CreateModel(
            name='BranchConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('service_id', models.IntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mkridit.branch')),
            ],
        ),
    ]