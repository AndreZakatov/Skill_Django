from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "avatar", "bio"
        widgets = {
            "avatar": forms.FileInput(attrs={"accept": "image/*"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }