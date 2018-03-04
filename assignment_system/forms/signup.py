from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Firstname'
            }
        )
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Lastname'
            }
        )
    )
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        ),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password again'
            }
        ),
        label="Password confirmation"
    )

    """
    Workaround to use first part of the email as a username
    """
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = user.email.split('@')[0]
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'email', 'password1', 'password2'
        )
