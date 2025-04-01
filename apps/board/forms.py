from django import forms
from django.contrib.auth.models import User

from .models import Board, BoardMember


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["title", "description"]


class BoardMemberForm(forms.ModelForm):
    email = forms.EmailField(
        label="Member's Email",
        help_text="Enter the email address of the user you want to invite.",
    )

    class Meta:
        model = BoardMember
        fields = ["role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].widget.attrs.update({"class": "select w-full"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No user found with this email address.")
        return email
