# Generated by Django 5.0.6 on 2024-05-10 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_owner_groupchat_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GroupChat',
            new_name='Group',
        ),
    ]