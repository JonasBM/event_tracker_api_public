# Generated by Django 3.1.2 on 2020-10-02 20:45

from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension

class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0001_initial'),
    ]

    operations = [
	UnaccentExtension()
    ]
