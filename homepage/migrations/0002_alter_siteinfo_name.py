# Generated by Django 3.2.4 on 2021-07-14 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteinfo',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
