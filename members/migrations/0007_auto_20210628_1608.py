# Generated by Django 3.2.4 on 2021-06-28 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20210625_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactneedworking',
            name='need',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='reactneedworking',
            name='need_met',
            field=models.TextField(null=True),
        ),
    ]
