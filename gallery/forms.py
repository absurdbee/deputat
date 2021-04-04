from gallery.models import Album, Photo, PhotoComment
from django import forms


class AlbumForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))
	class Meta:
		model = Album
		fields = ['title', 'description', 'is_public', 'order', ]
