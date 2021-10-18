from django import forms
from django.contrib.auth.forms import UserCreationForm
from api.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        # https://stackoverflow.com/a/46283680 - CC BY-SA 3.0
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    github = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=255, required=True)
    displayName = forms.CharField(max_length=30, required=True)

    def save(self, commit=True):
        if commit:
            user = get_user_model().objects.create_user(email=self.cleaned_data["email"], displayName=self.cleaned_data[
                "displayName"], github=self.cleaned_data["github"], password=self.cleaned_data["password1"], type="author")
        return user

    class Meta:
        model = User
        fields = ('displayName', 'email', 'github', 'password1', 'password2')
