from music.models import Music, SoundList
from django import forms
from music.helpers import validate_file_extension


class PlaylistForm(forms.ModelForm):

	class Meta:
		model = SoundList
		fields = ['name', 'order']

class TrackForm(forms.ModelForm):
	file = forms.FileField(validators=[validate_file_extension])
	class Meta:
		model = Music
		fields = ['title', 'file', 'list', ]
