from .models import CustomUser, Table, Bookings, TimeSlots
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions


class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['user','booking_date','booking_time',]
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
            'table': forms.Select(attrs={'class': 'form-control'}),
        
        }
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user',
            'booking_date',
            'booking_time',
            'table',
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )

