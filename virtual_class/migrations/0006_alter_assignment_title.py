# Generated by Django 4.1.4 on 2022-12-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_class', '0005_topic_faculty_subject_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]