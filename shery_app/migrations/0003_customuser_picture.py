# Generated by Django 5.0.6 on 2024-11-22 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shery_app', '0002_remove_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True,default=None, null=True, upload_to='media/profile_pictures'),
        ),
    ]
