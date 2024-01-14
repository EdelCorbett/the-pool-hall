from django.contrib import admin
from django.urls import path, include
from poolhall.views import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
    path('blog/', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('allauth.urls')),
]

handler404 = 'poolhall.views.handler404'
handler500 = 'poolhall.views.handler500'


