from organizations.models import Organization
from django import forms


class OrganizationForm(forms.ModelForm):
	class Meta:
		model = Organization
		fields = ['name', 'city', 'image', 'category', 'email_1','email_2', 'phone_1', 'phone_2', 'address_1', 'address_2', 'type', 'description',] 
