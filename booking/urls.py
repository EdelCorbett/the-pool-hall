from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('booking/', views.bookingView.as_view(), name='booking'),
]
