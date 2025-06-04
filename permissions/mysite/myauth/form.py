from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomRegistrationForm(UserCreationForm):

    bio = forms.CharField(
        max_length=500,
        required=False,
        widget = forms.Textarea(attrs={'rows': 3}),
        help_text="Расскажи о себе",
    )

    agreement_accepted = forms.BooleanField(
        required=True,
        label="Согласие с условиями использования",
        help_text="Принять условие и продолжить",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "bio", "agreement_accepted")