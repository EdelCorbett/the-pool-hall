from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('view_booking/', views.ViewBookingsView.as_view(),
         name='view_booking'),
    path('account/signup/', views.MemberRegisterView.as_view(),
         name='accounts_signup'),
    path('edit_booking/<int:booking_id>/', views.EditBookingView.as_view(),
         name='edit_booking'),
    path('cancel_booking/<int:booking_id>/', views.CancelBookingView.as_view(),
         name='cancel_booking'),
         ]

