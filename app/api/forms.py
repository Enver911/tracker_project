from django import forms
from tracker.models import Board, Card

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ("avatar", "background")
        
        
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ("avatar", "background")