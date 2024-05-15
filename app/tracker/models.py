from django.db import models
from django.contrib.auth import get_user_model


def board_upload_to(instance, filename):
    return f"{instance.author.username}/boards/filename"

def card_upload_to(instance, filename):
    return f"{instance.author.username}/cards/filename"

# Create your models here.
class Board(models.Model):
    author = models.ManyToManyField(to=get_user_model(), related_name="boards")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    background = models.ImageField(upload_to=board_upload_to, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class Column(models.Model):
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name="columns")
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Card(models.Model):
    column = models.ForeignKey(to=Column, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    background = models.ImageField(upload_to=card_upload_to, null=True, blank=True) # исправить
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title