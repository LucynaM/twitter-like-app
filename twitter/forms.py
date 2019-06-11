from django import forms
from django.core.exceptions import ValidationError
from .models import Tweet, MyUser, Comments, Messages


class EntryForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ['user', 'banned']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class SigninForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password2', 'first_name', 'last_name']

    def clean(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Hasła są różne')
        return self.cleaned_data

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        labels = {'content': 'komentarz'}


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['message', ]
        labels = {
            'message': '',
        }

