# Generated by Django 5.0.6 on 2024-05-17 23:53

import tracker.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_alter_board_background_alter_card_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=tracker.models.card_avatar),
        ),
    ]
