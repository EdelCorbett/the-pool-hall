from django.utils import timezone
from datetime import timedelta, datetime
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import BookingForm, MemberForm
from .models import Table, Bookings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Index view
class IndexView(TemplateView):
    template_name = 'index.html'


# Member register view
class MemberRegisterView(FormView):
    """
    View for member registration
    Creates a new user and saves it to the database
    set is_membership_approved to False so that the admin can approve
    the membership
    call the form_valid method of the super class
    if the form is invalid, call the form_invalid method
    of the super class which will render the form validation errors
    """
    template_name = 'accounts_signup.html'
    form_class = MemberForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_membership_approved = False
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class BookingBaseView(LoginRequiredMixin, View):
    def is_table_available(self, table, booking_date, booking_time):
        booking_start_time = datetime.combine(booking_date, booking_time)
        booking_end_time = booking_start_time + timedelta(hours=1)
        overlapping_bookings = Bookings.objects.filter(
            table=table,
            is_cancelled=False,
            booking_date=booking_date,
            booking_time__lt=booking_end_time.time(),
            booking_end_time__gt=booking_start_time.time()
        )

        return overlapping_bookings.count() == 0


class BookingView(BookingBaseView, FormView):
    """
    Booking view render the booking.html template with the booking form
    the get method renders the booking form and passes it to the template
    the post method checks if membership is approved if not,
    it redirects to the index page with an error message
    if membership is approved it processes the form
    """
    template_name = 'booking.html'
    form_class = BookingForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_membership_approved:
            messages.error(request,
                           'Your membership is not approved yet.'
                           'Bookings can only be made by approved members.')
            return redirect('index')

        form_data = request.POST.copy()
        form_data['user'] = request.user.id
        form = self.form_class(form_data)

        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']
            print(booking_date)

            booking_date_str = booking_date.strftime('%d-%m-%y')
            booking_time_str = booking_time.strftime('%H:%M')

            table_available = False

            for table in Table.objects.filter():
                if self.is_table_available(table, booking_date, booking_time):
                    booking = form.save(commit=False)
                    booking.table = table
                    booking.user = request.user
                    booking.save()

                    booking_datetime = datetime.combine(
                        booking_date, booking_time)
                    booking_datetime_aware = timezone.make_aware(
                        booking_datetime)

                    booking.booking_end_time = (
                        booking_datetime_aware + timedelta(hours=1)
                    )
                    booking.save()

                    table.booked_start_time = booking_datetime_aware
                    table.booked_end_time = booking_datetime_aware + timedelta(
                        hours=1)
                    table.is_available = False
                    table.save()

                    table_available = True
                    break

            if table_available:
                messages.success(
                    request,
                    f"Booking successful for {booking_date_str}"
                    f"at {booking_time_str}")
                return redirect('view_booking')

            else:
                form = self.form_class(initial=request.POST)
                return render(
                    request, self.template_name, {
                        'form': form, 'error_message':
                        "No tables available for the selected date and time."})
        else:
            return render(request, self.template_name, {'form': form})


class ViewBookingsView(LoginRequiredMixin, View):
    """
    View for viewing all bookings of a user
    gets all the bookings of the user and passes it to
    the view_booking.html template
    """
    template_name = 'view_booking.html'

    def get(self, request):
        cancelled_bookings = Bookings.objects.filter(
            user=request.user, is_cancelled=True).order_by('-booking_date')[:5]
        upcoming_bookings = Bookings.objects.filter(
            user=request.user, is_cancelled=False,
            booking_date__gte=timezone.now()).order_by('booking_date')
        past_bookings = Bookings.objects.filter(
            user=request.user, is_cancelled=False,
            booking_date__lt=timezone.now()).order_by('-booking_date')[:5]
        return render(request, self.template_name, {
            'cancelled_bookings': cancelled_bookings,
            'upcoming_bookings': upcoming_bookings,
            'past_bookings': past_bookings})


# Edit booking view
class EditBookingView(BookingBaseView):
    """
    View for editing a booking
    gets the booking from the database with booking_id and
    passes it to the edit_booking.html template
    if no booking is found, it returns a 404 error
    create a form instance with the booking data
    updates the booking with the new data
    if the form is valid, it redirects to the view_booking
    """
    template_name = 'edit_booking.html'

    def get(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        form = BookingForm(instance=booking)
        return render(request, self.template_name, {
            'form': form, 'booking': booking})

    def post(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        form = BookingForm(request.POST, instance=booking)

        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']

            # Check if the booking date is in the future
            if booking_date < datetime.now().date():
                form.add_error('booking_date',
                               'Booking date must be in the future.')
                return render(
                    request, self.template_name, {
                        'form': form, 'booking': booking})

            # Check if the table is available
            table = booking.table
            if not self.is_table_available(table, booking_date, booking_time):
                form.add_error(
                    None, 'Table is not available at the selected time.')
                return render(
                    request, self.template_name, {
                        'form': form, 'booking': booking})

            form.save()
            messages.success(request,
                             'You have successfully edited your booking.')
            return redirect('view_booking')
        else:
            return render(
                request, self.template_name, {
                    'form': form, 'booking': booking})


# Cancel booking view
class CancelBookingView(LoginRequiredMixin, View):
    """
    View for canceling a booking
    gets the booking from the database with booking_id and
    passes it to the cancel_booking.html template
    if no booking is found, it returns a 404 error
    updates the booking to mark it as cancelled
    updates the table to mark it as available
    redirects to the view_booking page with a success message
    """
    template_name = 'cancel_booking.html'

    def get(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        form = BookingForm(instance=booking)
        warning_message = 'Please note canceling a booking is irreversible'
        return render(request, self.template_name, {
            'form': form, 'warning_message': warning_message})

    def post(self, request, booking_id):
        booking = get_object_or_404(Bookings, id=booking_id)
        table = booking.table
        if table is not None:
            table.is_available = True
            table.save()
        booking.is_cancelled = True
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
        return redirect('view_booking')
