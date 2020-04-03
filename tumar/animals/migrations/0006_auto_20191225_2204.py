# Generated by Django 2.1.15 on 2019-12-25 16:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0005_auto_20191225_1754"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="machinery",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="machinery",
                to="animals.Farm",
                verbose_name="Farm",
            ),
        ),
    ]
