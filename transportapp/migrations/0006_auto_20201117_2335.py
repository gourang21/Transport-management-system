# Generated by Django 3.1.3 on 2020-11-17 18:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transportapp', '0005_tyrerecords'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TyreRecords',
            new_name='TyreRecord',
        ),
    ]