from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    name = forms.CharField(max_length=30, help_text='Required. Inform your name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Inform your last name')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    status = forms.CharField(max_length=30, help_text='Required. Inform your status')
    password1 = forms.CharField(max_length=30, help_text='Required. Inform your password.')
    password2 = forms.CharField(max_length=30, help_text='Required. Inform your password again.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name', 'birth_date', 'status', 'password1', 'password2')
