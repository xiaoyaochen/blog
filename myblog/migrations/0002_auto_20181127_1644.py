# Generated by Django 2.1 on 2018-11-27 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='Tag',
            new_name='tags',
        ),
    ]