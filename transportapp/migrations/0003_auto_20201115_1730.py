# Generated by Django 3.1.3 on 2020-11-15 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportapp', '0002_tripprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripprofile',
            name='good_type2',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tripprofile',
            name='good_type3',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tripprofile',
            name='good_type4',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tripprofile',
            name='good_type5',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tripprofile',
            name='good_type',
            field=models.CharField(default=None, max_length=200),
        ),
    ]