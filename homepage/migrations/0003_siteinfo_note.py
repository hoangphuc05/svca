# Generated by Django 3.2.4 on 2021-07-17 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_siteinfo_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]