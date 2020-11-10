from django import forms
from django.forms import FileInput, DateInput
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

# custom date input field, otherwise it would be plain text
class DateInput(forms.DateInput):
    input_type = 'date' # this overrides the default input type

class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }