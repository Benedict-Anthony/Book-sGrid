# Generated by Django 4.1 on 2022-09-09 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='write_about',
            field=models.TextField(max_length=200, verbose_name='what you write about'),
        ),
    ]
