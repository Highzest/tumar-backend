# Generated by Django 2.1.15 on 2020-03-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecalendar', '0002_auto_20200316_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breedingstockevent',
            name='completion_date',
            field=models.DateField(null=True, verbose_name='Date of the event completion'),
        ),
        migrations.AlterField(
            model_name='calfevent',
            name='completion_date',
            field=models.DateField(null=True, verbose_name='Date of the event completion'),
        ),
    ]
