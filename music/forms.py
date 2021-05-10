from music.models import Music, SoundList
from django import forms


class PlaylistForm(forms.ModelForm):

	class Meta:
		model = SoundList
		fields = ['name', 'order']

class TrackForm(forms.ModelForm):

	class Meta:
		model = Music
		fields = ['title', 'file', 'list', ]
