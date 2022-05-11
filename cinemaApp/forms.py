from django import forms
from django.forms import ModelForm
from .models import Session, Hall, Cinema
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ('name', 'start_time', 'end_time',
                  'description', 'cinema', 'hall', 'session_image')
        labels = {
            'name': '',
            'start_time': '',
            'end_time': '',
            'description': '',
            'cinema': '',
            'hall': '',
            'session_image': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie Name'}),
            'start_time': DateTimePickerInput(attrs={'placeholder': 'Start Time'}),
            'end_time': DateTimePickerInput(attrs={'placeholder': 'End Time'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        self.fields['session_image'].widget.attrs['class'] = 'form-control'
        self.fields['cinema'].widget.attrs['class'] = 'form-control'
        self.fields['hall'].widget.attrs['class'] = 'form-control'
        self.fields['hall'].queryset = Hall.objects.none()

        if 'cinema' in self.data:
            try:
                cinema_id = int(self.data.get('cinema'))
                self.fields['hall'].queryset = Cinema.objects.get(
                    id=cinema_id).halls.all()
            except (ValueError, TypeError):
                pass
