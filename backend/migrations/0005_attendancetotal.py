# Generated by Django 4.0.4 on 2022-09-17 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_attendanceclass_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student')),
            ],
            options={
                'unique_together': {('student', 'course')},
            },
        ),
    ]
