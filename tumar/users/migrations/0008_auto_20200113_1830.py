# Generated by Django 2.1.15 on 2020-01-13 12:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_auto_20200113_1705"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={
                    "unique": "A user with that phone number already exists."
                },
                help_text="Required. Phone number must be entered in the format: '+77076143537'. Up to 15 digits allowed.",
                max_length=16,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+77076143537' or '77076143537'. Up to 15 digits allowed.",
                        regex="^\\+\\d{11}$",
                    )
                ],
                verbose_name="phone number",
            ),
        ),
    ]
