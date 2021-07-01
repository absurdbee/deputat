from django import forms
from users.models import User
from users.model.settings import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserPasswordForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('password',)
class UserPhoneForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('phone',)
class UserKeyForm(forms.ModelForm):
	class Meta:
		model = UserSecretKey
		fields = ('key',)
class DeputatSendForm(forms.ModelForm):
	class Meta:
		model = DeputatSend
		fields = ('text',)

class UserNotifyForm(forms.ModelForm):
    class Meta:
        model = UserNotifications
        fields = ('comment','reaction','comment_reaction','reply','admin',)

class UserPrivateForm(forms.ModelForm):
    class Meta:
        model = UserPrivate
        fields = ('city','networks','subscribers','old','other',)

from users.model.profile import *
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('education','employment',)
