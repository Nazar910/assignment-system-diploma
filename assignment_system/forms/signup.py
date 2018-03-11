from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from assignment_system.models.taskowner import TaskOwner


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Ім\'я'
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Прізвище'
    )
    patronymic = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Побатькові'
    )
    position = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Посада'
    )
    email = forms.EmailField(
        max_length=254, help_text='Введіть коректну email-адресу.',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label="Введить пароль іще раз"
    )

    " Встановити строгий порядок полів у формі "
    field_order = [
        'first_name',
        'last_name',
        'patronymic',
        'position',
        'email',
        'password1',
        'password2',
    ]

    """
    Workaround to use first part of the email as a username
    """
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = user.email.split('@')[0]

        print('Patronymic')
        print(self.cleaned_data['patronymic'])

        """
        Ensure user to be in task-owners list
        """
        TaskOwner.objects.create(
            name=user.first_name,
            last_name=user.last_name,
            patronymic=self.cleaned_data['patronymic'],
            position=self.cleaned_data['position'],
            email=user.email
        )

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'email', 'password1', 'password2',
            'patronymic'
        )
