from django.forms import ModelForm
from .models import Contact, Place, Hotel, Room


class Contact(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class PlaceF(ModelForm):
    class Meta:
        model = Place
        fields = '__all__'

class HotelF(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

class Room(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'