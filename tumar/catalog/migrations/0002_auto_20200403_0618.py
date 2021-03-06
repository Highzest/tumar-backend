# Generated by Django 2.1.15 on 2020-04-03 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_description',
            field=models.TextField(blank=True, verbose_name='Short Company Description'),
        ),
        migrations.AlterField(
            model_name='company',
            name='emails',
            field=models.CharField(blank=True, max_length=100, verbose_name='Emails'),
        ),
        migrations.AlterField(
            model_name='company',
            name='facebook_url',
            field=models.CharField(blank=True, max_length=100, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='company',
            name='instagram_url',
            field=models.CharField(blank=True, max_length=100, verbose_name='Instagram'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone_numbers',
            field=models.CharField(blank=True, max_length=100, verbose_name='Phone Numbers'),
        ),
        migrations.AlterField(
            model_name='company',
            name='product_description',
            field=models.TextField(blank=True, verbose_name='Product Description'),
        ),
        migrations.AlterField(
            model_name='company',
            name='web_sites',
            field=models.CharField(blank=True, max_length=100, verbose_name='Websites'),
        ),
    ]
