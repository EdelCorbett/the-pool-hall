from datetime import timedelta, datetime, time
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import BookingForm, MemberForm
from .models import Table, Bookings, TimeSlots
from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class MemberRegisterView(FormView):
    template_name = 'accounts_signup.html'
    form_class = MemberForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_membership_approved = True
        user.save()
        return redirect('index')
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class BookingView(LoginRequiredMixin, FormView):
    template_name = 'booking.html'
    form_class = BookingForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'user': request.user})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
    
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']
            print(booking_date)

            table_available = False

            for table in Table.objects.filter():
                if self.is_table_available(table, booking_date, booking_time):
                    booking = form.save(commit=False)
                    booking.table = table
                    booking.user = request.user
                    booking.save()

                    booking_datetime = datetime.combine(booking_date, booking_time)

                    table.booked_start_time = booking_datetime
                    table.booked_end_time = table.booked_start_time + timedelta(hours=1)
                    table.is_available = False  # Mark the table as not available during the booked time
                    table.save()

                    table_available = True
                    break

            if table_available:
                return HttpResponse("Booking successful")
            else:
                return HttpResponse("No tables available")
        else:
            return render(request, self.template_name, {'form': form})
        
    def is_table_available(self, table, booking_date, booking_time):
        booking_datetime = datetime.combine(booking_date, booking_time)
        bookings = Bookings.objects.filter(
            booking_date=booking_date, booking_time=booking_time, table=table)
        return bookings.count() == 0


                    
                        

            
            
        


                        
                
                