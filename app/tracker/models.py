from django.db import models
from django.contrib.auth import get_user_model


def board_avatar(instance, filename):
    return f"boards/{instance.id}/avatar/{filename}" 


def card_avatar(instance, filename):
    return f"cards/{instance.id}/avatar/{filename}"


# Create your models here.
class Board(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="boards")
    title = models.CharField(max_length=100, default="No name")
    description = models.TextField(null=True)
    avatar = models.ImageField(upload_to=board_avatar, null=True)
    background = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.title
    
    
class Column(models.Model):
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name="columns")
    title = models.CharField(max_length=100, default="No name")
    
    def __str__(self):
        return self.title


class Card(models.Model):
    column = models.ForeignKey(to=Column, on_delete=models.CASCADE, related_name="cards")
    title = models.CharField(max_length=100, default="No name")
    description = models.TextField(null=True)
    avatar = models.ImageField(upload_to=card_avatar, null=True)
    background = models.CharField(max_length=100, null=True)
    foreground = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.title
    
    
class Follower(models.Model):
    class Permissions(models.TextChoices):
        MODERATOR = "Moderator"
        READER = "Reader"
    
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="follow_boards")
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name="followers")
    permission = models.CharField(choices=Permissions.choices, default=Permissions.READER)
    
    class Meta:
        unique_together = ("user", "board")