from gallery.models import PhotoList, Photo
from django import forms


class PhotoListForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))
	class Meta:
		model = PhotoList
		fields = ['name', 'description', 'order', ]
