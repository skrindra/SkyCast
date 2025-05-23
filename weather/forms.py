from django import forms
from .models import WeatherQuery
from datetime import date

class WeatherQueryForm(forms.ModelForm):
    class Meta:
        model = WeatherQuery
        fields = ['location', 'start_date', 'end_date']
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter city name, zip code, or coordinates'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'max': date.today().isoformat()  # Set max date to today for start date
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
                # No max date for end date to allow future dates
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default dates
        today = date.today()
        self.fields['start_date'].initial = today
        self.fields['end_date'].initial = today

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        location = cleaned_data.get('location')

        if not location:
            raise forms.ValidationError("Please enter a location")

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after or equal to start date")
            
            # Only validate start date to be today or past
            today = date.today()
            if start_date > today:
                raise forms.ValidationError("Start date cannot be in the future")
            # No validation for end date to allow future dates

        return cleaned_data

class WeatherSearchForm(forms.Form):
    location = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter city name, zip code, or coordinates',
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location or location.strip() == '':
            raise forms.ValidationError("Please enter a location")
        return location.strip() 