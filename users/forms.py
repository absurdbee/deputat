from django import forms
from users.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserPasswordForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('password',)
