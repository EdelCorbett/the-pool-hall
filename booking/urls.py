from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('account/signup/', views.MemberRegisterView.as_view(), name='accounts_signup'),
    
]
