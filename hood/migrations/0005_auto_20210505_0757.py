# Generated by Django 3.2.1 on 2021-05-05 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hood', '0004_auto_20210505_0638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='prof_picture',
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
