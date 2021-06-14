# Generated by Django 3.2.4 on 2021-06-14 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reactmember',
            options={'managed': False, 'permissions': [('is_member', 'Is a member and conly view specific information')]},
        ),
        migrations.AlterModelOptions(
            name='reactuser',
            options={'managed': False, 'permissions': [('is_user', 'Is a user and can most information related to react app')]},
        ),
    ]
