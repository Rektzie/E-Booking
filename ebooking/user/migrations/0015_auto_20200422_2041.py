# Generated by Django 3.0.5 on 2020-04-22 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_userrole_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_student',
            name='staff_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='booking_student',
            name='teacher_date',
            field=models.DateTimeField(blank=True),
        ),
    ]