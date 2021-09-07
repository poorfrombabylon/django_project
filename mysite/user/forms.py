from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _


class NewUserForm(forms.ModelForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    first_name = forms.CharField(label=_('Name'), strip=False)
    last_name = forms.CharField(label=_('Last name'), strip=False)
    email = forms.EmailField(label=_('Email Address'))

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
