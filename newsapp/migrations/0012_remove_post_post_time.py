# Generated by Django 3.2.8 on 2021-10-25 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0011_post_post_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_time',
        ),
    ]