# Generated by Django 4.1.13 on 2023-12-31 04:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_users_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
