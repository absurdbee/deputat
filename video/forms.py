from video.models import VideoList, Video
from django import forms


class VideoListForm(forms.ModelForm):

	class Meta:
		model = VideoList
		fields = ['name', 'order']

class VideoForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))

	class Meta:
		model = Video
		fields = ['title', 'file', 'image' 'list', ]
