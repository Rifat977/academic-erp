# Generated by Django 4.0.4 on 2022-09-20 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_studentcourse_marksclass_marks'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]
