# Generated by Django 3.2.8 on 2021-10-25 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0010_register_table_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]