# Generated by Django 2.1.15 on 2020-05-10 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0019_auto_20200509_2134'),
        ('ecalendar', '0005_auto_20200509_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleBreedingStockEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed?')),
                ('completion_date', models.DateField(null=True, verbose_name='Date of the event completion')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animals.BreedingStock')),
            ],
        ),
        migrations.CreateModel(
            name='SingleCalfEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed?')),
                ('completion_date', models.DateField(null=True, verbose_name='Date of the event completion')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animals.Calf')),
            ],
        ),
        migrations.RemoveField(
            model_name='breedingstockevent',
            name='animal',
        ),
        migrations.RemoveField(
            model_name='breedingstockevent',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='breedingstockevent',
            name='completion_date',
        ),
        migrations.RemoveField(
            model_name='calfevent',
            name='animal',
        ),
        migrations.RemoveField(
            model_name='calfevent',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='calfevent',
            name='completion_date',
        ),
        migrations.AddField(
            model_name='singlecalfevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecalendar.CalfEvent'),
        ),
        migrations.AddField(
            model_name='singlebreedingstockevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecalendar.BreedingStockEvent'),
        ),
        migrations.AddField(
            model_name='breedingstockevent',
            name='animals',
            field=models.ManyToManyField(related_name='events', through='ecalendar.SingleBreedingStockEvent', to='animals.BreedingStock', verbose_name='Cow Animal of the event'),
        ),
        migrations.AddField(
            model_name='calfevent',
            name='animals',
            field=models.ManyToManyField(related_name='events', through='ecalendar.SingleCalfEvent', to='animals.Calf', verbose_name='Calf Animal of the event'),
        ),
    ]