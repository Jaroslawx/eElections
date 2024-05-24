from captcha.fields import CaptchaField
from datetime import datetime, date

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms import SelectDateWidget


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    name = forms.CharField(
        max_length=30,
        help_text='Required. Inform your name.',
        widget=forms.TextInput(attrs={'placeholder': 'Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        help_text='Required. Inform your last name.',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    birth_date = forms.DateField(
        widget=SelectDateWidget(
            years=range(1930, datetime.now().year - 13),
            attrs={'placeholder': 'Birth Date'}
        ),
        help_text='Required. Choose your birth date'
    )
    password1 = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text='Required. Inform your password.'
    )
    password2 = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text='Required. Inform your password again.'
    )
    captcha = CaptchaField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError('You must be at least 18 years old to register.')
        return birth_date

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name', 'birth_date', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }


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
