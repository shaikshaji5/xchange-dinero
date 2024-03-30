# registration/forms.py
from django import forms
from .models import profile, AddQuery
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )  # here we use passwordinput to hide the characters that user enters


class Userregistrationform(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm_passowrd", widget=forms.PasswordInput)

    # photo = forms.ImageField(label = 'Photo')
    class Meta:
        model = User
        # fields = {'username','email'}
        fields = ["username", "email"]

    def check_passowrd(self):
        if self.cleaned_data["password"] != self.cleaned_data["password2"]:
            raise forms.ValidationError("passwords donot match")
        return self.cleaned_data["password2"]


class Usereditform(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileEditform(forms.ModelForm):
    class Meta:
        model = profile
        fields = ["Roll", "call"]


class AddQueryForm(forms.ModelForm):
    class Meta:
        model = AddQuery
        fields = [
            "name",
            "registration_number",
            "phone_number",
            "checkbox_field",
            "radio_field",
        ]
        widgets = {
            "checkbox_field": forms.CheckboxInput(),
        }
