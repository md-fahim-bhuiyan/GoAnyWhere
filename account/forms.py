from django.forms import ModelForm
from .models import Contact


class Contact(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'