from django.forms import ModelForm
from .models import Contact, Place


class Contact(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class Place(ModelForm):
    class Meta:
        model = Place
        fields = '__all__'