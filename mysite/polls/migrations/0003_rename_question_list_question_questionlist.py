# Generated by Django 3.2.5 on 2021-07-26 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20210726_1425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_list',
            new_name='questionlist',
        ),
    ]