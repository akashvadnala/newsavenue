# Generated by Django 3.2.8 on 2021-10-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0009_alter_post_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_table',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
