# Generated by Django 5.0.6 on 2024-05-20 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_card_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='foreground',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
