from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.'
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.'
    )
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.'
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
