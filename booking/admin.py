from django.contrib import admin
from .models import CustomUser, Table, Bookings, TimeSlots
# Register your models here.
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('booking_date', 'booking_time', 'table' , 'user',"is_cancelled")
    list_filter = ('booking_date', 'booking_time', 'table' , 'user',"is_cancelled")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_cancelled=False)
    

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'username','is_staff', 'membership_id')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'membership_id')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(membership_id=1)

    def has_add_permission(self, request):
        return True 
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Table)
admin.site.register(Bookings, BookingsAdmin)
admin.site.register(TimeSlots)