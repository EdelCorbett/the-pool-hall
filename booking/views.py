from django.utils import timezone
from datetime import timedelta, datetime
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import BookingForm, MemberForm
from .models import Table, Bookings, TimeSlots
from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

# Member register view
class MemberRegisterView(FormView):
    template_name = 'accounts_signup.html'
    form_class = MemberForm
# IF form is valid,membership is approved,save the user and redirect to index page
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_membership_approved = True
        user.save()
        return redirect('index')
#If form is invalid,print the errors    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

# Booking view
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
                    booking_datetime_aware = timezone.make_aware(booking_datetime)

                    table.booked_start_time = booking_datetime_aware
                    table.booked_end_time = booking_datetime_aware + timedelta(hours=1)
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
    
class ViewBookingsView(LoginRequiredMixin,View):
    template_name = 'view_booking.html'

    def get(self, request):
        user_bookings = Bookings.objects.filter(user=request.user)
        return render(request, self.template_name, {'bookings': user_bookings})
    

# Edit booking view
class EditBookingView(LoginRequiredMixin,View):
    template_name = 'edit_booking.html'

   
    def get(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        form = BookingForm(instance=booking)
        return render(request, self.template_name, {'form': form, 'booking': booking})

    def post(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        form = BookingForm(request.POST, instance=booking)
        
        if form.is_valid():
            form.save()
            return redirect('view_booking') 
        
        return render(request, self.template_name, {'form': form, 'booking': booking})
    
# Cancel booking view
class CancelBookingView(LoginRequiredMixin,View):
    template_name = 'cancel_booking.html'
    

    def get(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        warning_message = "Please note that canceling a booking is irreversible."
        return render(request, self.template_name, {'booking': booking, 'warning_message': warning_message})

    def post(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        booking.is_cancelled = True
        booking.save()

        table = booking.table
        table.is_available = True  # Mark the table as available
        table.save()

        success_message = "Your booking was successfully canceled."
        messages.success(request, success_message)


        return redirect('view_booking')
                    
                        

            
            
        


                        
                
                