from django.db import models
from django.contrib.auth import get_user_model


def board_avatar(instance, filename):
    return f"boards/{instance.id}/avatar/{filename}" 

def card_avatar(instance, filename):
    return f"cards/{instance.id}/avatar/{filename}"

def board_background(instance, filename):
    return f"{instance.author.username}/boards/background/{filename}"

def card_background(instance, filename):
    return f"{instance.author.username}/cards/background/{filename}"

# Create your models here.
class Board(models.Model):
    author = models.ManyToManyField(to=get_user_model(), related_name="boards")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    avatar = models.ImageField(upload_to=board_avatar, null=True)
    background = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.title
    
class Column(models.Model):
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name="columns")
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Card(models.Model):
    column = models.ForeignKey(to=Column, on_delete=models.CASCADE, related_name="cards")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    avatar = models.ImageField(upload_to=card_avatar, null=True)
    background = models.CharField(max_length=100, null=True)
    foreground = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.title