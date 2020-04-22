# Generated by Django 3.0.5 on 2020-04-19 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_student_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='role',
            field=models.IntegerField(choices=[(1, 'นักศึกษา'), (2, 'อาจารย์'), (3, 'บุลคลากร')], default=1),
        ),
    ]
