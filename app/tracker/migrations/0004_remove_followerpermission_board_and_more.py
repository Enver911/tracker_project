# Generated by Django 5.0.6 on 2024-05-21 12:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_permission_followerpermission'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followerpermission',
            name='board',
        ),
        migrations.RemoveField(
            model_name='followerpermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='followerpermission',
            name='user',
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('1', 'Moderator'), ('2', 'Reader')], default='2')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='tracker.board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_boards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='FollowerPermission',
        ),
    ]