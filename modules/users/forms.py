from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm
from django.utils.translation import gettext as _

from modules.users.models import Rangs, Dzial, Server, UsersProfile
from modules.users.models import PanelUser


class ForgotForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
                "type": "email",
                "autocomplete": "email"
            }
        ))

    class Meta:
        model = PanelUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            PanelUser.objects.get(email=email)
        except PanelUser.DoesNotExist:
            raise forms.ValidationError(_('This e-mail address doesnt exist'))

        return email


class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                'type': 'password',
                'autocomplete': 'new-password'
            }
        ),
        error_messages={'required': _('You must set a strong password!')})
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
                'type': 'password',
                'autocomplete': 'new-password'
            }
        ),
        error_messages={'required': _('The two password fields didn\'t match.')})

    class Meta:
        model = PanelUser
        fields = ('password1', 'password2')

    def clean(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 != password2:
            raise forms.ValidationError('password mismatch')


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nazwa Użytkownika",
                "class": "form-control",
                "autocomplete": "username"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Hasło",
                "class": "form-control",
                "autocomplete": "current-password"
            }
        ))

    remember = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "id": "remember",
            }
        ))


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
                "autocomplete": "username",
            }
        ),
        error_messages={'required': _('The username is required')})
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
                "autocomplete": "email"
            }
        ),
        error_messages={'required': _('You must set your E-Mail address')})
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control",
                "autocomplete": "given-name"
            }
        ),
        error_messages={'required': _('Your First name is required')})

    class Meta:
        model = PanelUser
        fields = ['username', 'email', 'first_name']

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.is_active = False
        user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            PanelUser.objects.get(email=email)
        except PanelUser.DoesNotExist:
            return email

        raise forms.ValidationError(_('This e-mail address is used by another user!'))


class CreateProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=UsersProfile.GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                "placeholder": "Gender",
                "class": "form-control",
                "autocomplete": "sex"
            }
        )
    )
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "Birthday",
                "class": "form-control",
                'type': 'date',
                "autocomplete": "bday"
            }
        )
    )
    ranga = forms.ModelChoiceField(
        empty_label='Wybierz range',
        queryset=Rangs.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "autocomplete": "ranga"
            }
        )
    )
    dzial = forms.ModelChoiceField(
        empty_label='Wybierz dzial',
        queryset=Dzial.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "autocomplete": "dzial"
            }
        )
    )
    serwer = forms.ModelChoiceField(
        empty_label='Wybierz serwer',
        queryset=Server.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "autocomplete": "Serwer"
            }
        )
    )

    class Meta:
        model = UsersProfile
        fields = ['gender', 'birthday', 'ranga', 'serwer', 'dzial']


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
                "autocomplete": "username",
            }
        ),
        error_messages={'required': _('The username is required'),
                        'unique': "This username has already been registered."})
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
                "autocomplete": "email"
            }
        ),
        error_messages={'required': _('You must set your E-Mail address'),
                        'unique': "This email has already been registered."})

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control",
                "autocomplete": "given-name"
            }
        ),
        error_messages={'required': _('Your First name is required')})

    class Meta:
        model = PanelUser
        fields = ['username', 'email', 'first_name']


class ProfileEditForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=UsersProfile.GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                "placeholder": "Gender",
                "class": "form-control",
                "autocomplete": "sex"
            }
        )
    )
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "Birthday",
                "class": "form-control",
                'type': 'date',
                "autocomplete": "bday"
            }
        )
    )
    ranga = forms.ModelChoiceField(
        empty_label=Rangs.objects.all().first(),
        queryset=Rangs.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "autocomplete": "ranga"
            }
        )
    )
    dzial = forms.ModelChoiceField(
        empty_label=Dzial.objects.all().first(),
        queryset=Dzial.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "autocomplete": "dzial"
            }
        )
    )
    serwer = forms.ModelChoiceField(
        empty_label=Server.objects.all().first(),
        queryset=Server.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "autocomplete": "Serwer"
            }
        )
    )

    class Meta:
        model = UsersProfile
        fields = ['gender', 'birthday', 'ranga', 'serwer', 'dzial']
