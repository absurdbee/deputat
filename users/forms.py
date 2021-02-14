from django import forms
from users.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar','first_name', 'last_name', 'email')
