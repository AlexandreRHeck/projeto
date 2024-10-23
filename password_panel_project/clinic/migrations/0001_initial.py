# Generated by Django 5.1.2 on 2024-10-20 06:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Attendant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('time_called', models.DateTimeField(blank=True, null=True)),
                ('counter', models.IntegerField(blank=True, null=True)),
                ('called', models.BooleanField(default=False)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.clinic')),
            ],
        ),
    ]
