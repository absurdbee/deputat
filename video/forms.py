from video.models import VideoAlbum, Video
from django import forms


class VideolistForm(forms.ModelForm):

	class Meta:
		model = VideoAlbum
		fields = ['name', 'order']

class VideoForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))

	class Meta:
		model = Video
		fields = ['title', 'file', 'album', ]
