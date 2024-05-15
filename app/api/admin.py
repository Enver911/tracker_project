from django.contrib import admin
from tracker import models

# Register your models here.
admin.site.register(models.Board)
admin.site.register(models.Column)
admin.site.register(models.Card)