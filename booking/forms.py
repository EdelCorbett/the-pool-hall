from datetime import datetime, timedelta, date, time
from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.layout import  Submit
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.forms import UserCreationForm
import secrets
import string
from .models import CustomUser, Table, Bookings, TimeSlots


class MemberForm(UserCreationForm):
    email = forms.EmailField(required=False)
    membership_id = forms.CharField(max_length=10, required=False)

    class Meta:
        model = CustomUser
        fields = ("username","email", "password1", "password2", "membership_id")

    def clean(self):
        cleaned_data = super().clean()
        membership_id = cleaned_data.get('membership_id')

        if not membership_id or membership_id.strip() == '':
            while True:
                new_membership_id = ''.join(secrets.choice(
                    string.ascii_uppercase + string.digits) 
                    for _ in range(10))
                if not CustomUser.objects.filter(
                    membership_id=new_membership_id).exists():
                    cleaned_data['membership_id'] = new_membership_id
                    break

        return cleaned_data

    def try_save(self, commit=True):
        user = super(MemberForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.membership_id = self.cleaned_data.get('membership_id')

        if commit:
            user.save()

        resp = None 
        return user, resp
            
class TimeSlotForm(forms.Form):
    timeslots = forms.ChoiceField(choices=[(f'{hour:02}:{minute:02}', f'{hour:02}:{minute:02}') for hour in range(15, 22) for minute in range(0, 60, 15)])

    
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['user', 'booking_date','booking_time',]
        widgets = {
            'user': forms.TextInput(attrs={'readonly': 'readonly'}), 
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time','format': '%H:%M'}),
            'table': forms.Select(attrs={'class': 'form-control'}),
            
        
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')

        if booking_date < date.today():
            raise ValidationError("The date cannot be in the past!")

        return booking_date
    
    

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user

        

        FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        # )

    