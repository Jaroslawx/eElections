from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from base.forms import SignUpForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm


class SignUpFormTest(TestCase):
    def test_signup_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'name': 'New',
            'last_name': 'User',
            'birth_date': '2000-01-01',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'captcha': 'test'  # Use a test key for captcha during tests
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_no_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 8)

    def test_signup_form_email_already_exists(self):
        User.objects.create_user(username='existinguser', email='existinguser@example.com', password='password')
        form = SignUpForm(data={
            'username': 'newuser',
            'email': 'existinguser@example.com',
            'name': 'New',
            'last_name': 'User',
            'birth_date': '2000-01-01',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'captcha': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_signup_form_underage_user(self):
        birth_date = date.today().replace(year=date.today().year - 15)
        form = SignUpForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'name': 'New',
            'last_name': 'User',
            'birth_date': birth_date,
            'password1': 'newpassword',
            'password2': 'newpassword',
            'captcha': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)


class CustomAuthenticationFormTest(TestCase):
    def test_authentication_form_placeholders(self):
        form = CustomAuthenticationForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Username')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Password')


class CustomPasswordResetFormTest(TestCase):
    def test_password_reset_form_placeholders(self):
        form = CustomPasswordResetForm()
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email address')
        self.assertEqual(form.fields['email'].widget.attrs['class'], 'w-full p-2 ml-2 border-black border-2')


class CustomSetPasswordFormTest(TestCase):
    def test_set_password_form_placeholders(self):
        form = CustomSetPasswordForm()
        self.assertEqual(form.fields['new_password1'].widget.attrs['placeholder'], 'Password')
        self.assertEqual(form.fields['new_password1'].widget.attrs['class'], 'w-full p-2 ml-2 border-black border-2')
        self.assertEqual(form.fields['new_password2'].widget.attrs['placeholder'], 'Password confirmation')
        self.assertEqual(form.fields['new_password2'].widget.attrs['class'], 'w-full p-2 ml-2 border-black border-2')
