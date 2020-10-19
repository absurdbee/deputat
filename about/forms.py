from django import forms
from about.models import Feedback


class FeedbackForm(forms.ModelForm):
    name = forms.CharField( label="",widget=forms.TextInput(
            attrs={'class': 'hover-target', 'placeholder': ' Ваше имя'}
        ))
    email = forms.EmailField( label="",widget=forms.EmailInput(
            attrs={'class': 'hover-target', 'placeholder': 'Ваша почта'}
        ))
    message = forms.CharField( label="",widget=forms.Textarea(
            attrs={'class': 'hover-target', 'placeholder': 'Ваше сообщение','rows':'0','cols':'0','style':'height: 84px;'}
        ))
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
