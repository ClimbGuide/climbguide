# Generated by Django 3.1.2 on 2020-10-12 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201011_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='media/default-avatar-profile-image-vector-social-media-user-icon-potrait-182347582.jpg', null=True, upload_to='users/'),
        ),
    ]
