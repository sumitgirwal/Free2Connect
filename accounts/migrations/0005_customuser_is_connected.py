# Generated by Django 4.2.2 on 2023-06-14 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_groups_alter_customuser_interests_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_connected',
            field=models.BooleanField(default=False),
        ),
    ]
