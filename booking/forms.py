
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.forms import UserCreationForm
import secrets
import string
from .models import CustomUser, Table, Bookings, TimeSlots


class MemberForm(UserCreationForm):
    email = forms.EmailField(required=False)
    membership_id = forms.CharField(max_length=10, required=True)

    class Meta:
        model = CustomUser
        fields = ("username","email", "password1", "password2", "membership_id")
        def save(self, commit=True):
            user = super(MemberForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.membership_id = self.cleaned_data['membership_id']

            if not user.membership_id:
                while True:
                    new_membership_id = ''.join(secrets.choice(
                        string.ascii_uppercase + string.digits) 
                        for _ in range(10))
                    if not CustomUser.objects.filter(
                        membership_id=new_membership_id).exists():
                        user.membership_id = new_membership_id
                        break

            if commit:
                user.save()

            return user
    
class TimeSlotForm(forms.Form):
    timeslots = forms.ChoiceField(choices=[(f'{hour:02}:{minute:02}', f'{hour:02}:{minute:02}') for hour in range(15, 22) for minute in range(0, 60, 15)])

    
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['user', 'booking_date','booking_time','table']
        widgets = {
            'user': forms.HiddenInput(),
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time','format': '%H:%M'}),
            'table': forms.Select(attrs={'class': 'form-control'}),
            
        
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user

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

    