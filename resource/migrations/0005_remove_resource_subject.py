# Generated by Django 4.1.1 on 2022-09-12 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0004_rename_subjects_resource_subject_assignment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='subject',
        ),
    ]
