# Generated by Django 3.2.8 on 2021-10-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0005_auto_20211022_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(null=True, upload_to='img/covers'),
        ),
        migrations.AlterField(
            model_name='register_table',
            name='lastname',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
