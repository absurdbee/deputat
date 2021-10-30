from lists.models import MediaList
from django import forms


class MedialistForm(forms.ModelForm):

	class Meta:
		model = MediaList
		fields = ['name', 'order', 'parent']
