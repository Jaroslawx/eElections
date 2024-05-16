from datetime import datetime

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms import SelectDateWidget


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    name = forms.CharField(max_length=30, help_text='Required. Inform your name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Inform your last name')
    birth_date = forms.DateField(widget=SelectDateWidget(years=range(1930, datetime.now().year - 13)),
                                 help_text='Required. Choose your birth date')
    status = forms.ChoiceField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('staff', 'Staff')],
                               help_text='Required. Choose your status')
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput, help_text='Required. Inform your password.')
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput,
                                help_text='Required. Inform your password again.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name', 'birth_date', 'status', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email address'
        self.fields['email'].widget.attrs['class'] = 'w-full p-2 ml-2 border-black border-2'


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style = 'w-full p-2 ml-2 border-black border-2'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['new_password1'].widget.attrs['class'] = style
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Password confirmation'
        self.fields['new_password2'].widget.attrs['class'] = style
