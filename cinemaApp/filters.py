from .models import *
from django import forms
from django_filters import DateTimeFilter, CharFilter
import django_filters
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import Session


class SessionFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',
                      lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie Name'}))
    start_time = DateTimeFilter(
        field_name="start_time", lookup_expr='gte', label='', widget=DateTimePickerInput(attrs={'placeholder': 'Start Time'}))
    end_date = DateTimeFilter(field_name="end_time",
                              lookup_expr='lte', label='', widget=DateTimePickerInput(attrs={'placeholder': 'End Time'}))

    class Meta:
        model = Session
        fields = ('cinema', 'name')
        exclude = ['name']

        labels = {
            'name': '',
            'start_time': '',
            'end_time': '',
            'description': '',
            'cinema': '',
            'hall': '',
            'session_image': ''
        }
