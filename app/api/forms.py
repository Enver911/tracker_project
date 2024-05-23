from django import forms


class AvatarForm(forms.Form):
    avatar = forms.ImageField()
    
    def save(self, instance):
        instance.avatar.delete()
        instance.avatar = self.cleaned_data["avatar"]
        instance.save()
    
    
