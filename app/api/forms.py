from django import forms


class BoardForm(forms.Form):
    avatar = forms.ImageField()
    
    def save(self, instance):
        instance.avatar.delete()
        instance.avatar = self.cleaned_data["avatar"]
        instance.save()
    
    
class CardForm(forms.Form):
    avatar = forms.ImageField()
    
    def save(self, instance):
        instance.avatar.delete()
        instance.avatar = self.cleaned_data["avatar"]
        instance.save()
    
    
