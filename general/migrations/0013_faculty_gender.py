# Generated by Django 4.1.1 on 2022-11-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0012_subject_course_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='gender',
            field=models.CharField(blank=True, choices=[('', 'Choose Gender'), ('M', 'Male'), ('F', 'Female'), ('T', 'Transgender')], max_length=1),
        ),
    ]
