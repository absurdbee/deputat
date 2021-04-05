from video.models import VideoAlbum, Video, VideoComment
from django import forms


class AlbumForm(forms.ModelForm):

	class Meta:
		model = VideoAlbum
		fields = ['title', 'order']

class VideoForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder':'Описание'}))
	class Meta:
		model = Video
		fields = ['title', 'description', 'image', 'category', 'album', 'uri']
