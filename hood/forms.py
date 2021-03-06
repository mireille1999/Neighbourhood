from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User
class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ['user','location']
        
class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ['user','location']
        
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class notificationsForm(forms.ModelForm):
    class Meta:
        model = notifications
        exclude = ['author', 'neighbourhood', 'post_date']
   
   