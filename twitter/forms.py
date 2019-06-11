from django import forms
from django.core.exceptions import ValidationError
from .models import Tweet, MyUser, Comments, Messages


class EntryForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ['user', 'banned']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'tekst'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'email'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='')


class SigninForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password2'}), label='')

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password2', 'first_name', 'last_name']
        labels = {'email': '', 'first_name': '', 'last_name': ''}
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'nazwisko'}),
        }

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
        labels = {'content': ''}
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'komentarz'}),
        }


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['message', ]
        labels = {
            'message': '',
        }
