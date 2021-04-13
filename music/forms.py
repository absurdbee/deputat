from music.models import Music, SoundList
from django import forms


class PlaylistForm(forms.ModelForm):

	class Meta:
		model = SoundList
		fields = ['name', 'order']

class TrackForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))

	def clean_file(self):
		file = self.cleaned_data['file']
		try:
			if file:
				if len(file.name.split('.')) == 1:
					raise forms.ValidationError('File type is not supported')
				if file._size > settings.DOC_UPLOAD_FILE_MAX_SIZE:
					raise forms.ValidationError(_('Максимальный размер файла: %s. Ваш документ: %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
		except:
			pass
		return file

	class Meta:
		model = Music
		fields = ['title', 'file', 'list', ]
