from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from .forms import BookingForm
from .models import Table, Bookings, TimeSlots
from crispy_forms.helper import FormHelper


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class bookingView(TemplateView):
    template_name = 'booking.html'
    form_class = BookingForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            bookking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']
            table_available = False
            for table in Table.objects.all():
                if is_table_available(table,booking_date,booking_time):
                    booking = form.save(commit=False)
                    booking.table = table
                    booking.save()
                    table_available = True
                    break
            if table_available:
                return HttpResponse("Booking successful")
            else:
                return HttpResponse("No tables available")
                

        return render(request, self.template_name, {'form': form})
    




    