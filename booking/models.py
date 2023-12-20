from datetime import timedelta, datetime, time, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import secrets
import string



"""
Model for table number and if game size is singles or doubles
"""



class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=25)
    email = models.EmailField(blank=True, null=True,default=None)
    membership_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_membership_approved = models.BooleanField(default=False)
    membership_start_date = models.DateField(null=True, blank=True)
    membership_end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        #Check if membership_id is not provided
        if not self.membership_id:
            unique_membership_id = False
            #Generate a unique membership_id using secrets module
            while not unique_membership_id:
                new_membership_id = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                #Check if membership_id is unique
                if not CustomUser.objects.filter(membership_id=new_membership_id).exists():
                    self.membership_id = new_membership_id
                    unique_membership_id = True
                    #Calls the save method of the parent class of AbstractUser to save the instance

        super().save(*args, **kwargs)

class Table(models.Model):
    size_choices = (
        ('1', '1, singles'),
        ('2', '2, doubles'),
    )
    table_number = models.IntegerField(unique=True)
    table_size = models.CharField(choices=size_choices, default='1', max_length=2)
    booking_time = models.TimeField(null=True, blank=True)
    booked_start_time = models.DateTimeField(null=True, blank=True)
    booked_end_time = models.DateTimeField(null=True, blank=True)
    booking_date = models.DateField(null=True, blank=True)

    def is_table_available(self, booking_datetime, booking_size):
        booking_start_time = datetime.combine(booking_datetime.date(), self.booking_time)
        booking_end_time = booking_start_time + timedelta(hours=1)

        if (
            (self.booked_start_time is None or self.booked_start_time < booking_start_time)
            and (self.booked_end_time is None or self.booked_end_time < booking_start_time)
            and self.table_size == booking_size
        ):
            return True

        return False

    def __str__(self):
        return f"Table {self.table_number}"



class TimeSlots(models.Model):
    class Meta:
        verbose_name_plural = "Time slots"
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
]

    TIME_CHOICES = [
        ('15:00:00', '15:00:00'),
        ('16:00:00', '16:00:00'),
        ('17:00:00', '17:00:00'),
        ('18:00:00', '18:00:00'),
        ('19:00:00', '19:00:00'),
        ('20:00:00', '20:00:00'),
        ('21:00:00', '21:00:00'),
        ('22:00:00', '22:00:00'),
    ]
    
    day = models.CharField(choices=DAY_CHOICES, default='Monday',max_length=9)
    start_time =models.TimeField(choices=TIME_CHOICES, default='15:00:00')
    is_open = models.BooleanField(default=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE,related_name='timeslots')

    class Meta:
        unique_together = ('day', 'start_time', 'table')
        

    def __str__(self):
        return f"{self.get_day_display()} at {self.start_time.strftime('%H:%M')}"
    
    def get_all_tables(self):
        return self.table.all()
    
    def get_available_tables(self):
        return self.table.filter(is_open=True)
    
    def get_booked_tables(self):
        return self.table.filter(is_open=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if TimeSlots.objects.filter(day=self.day,start_time=self.start_time,table=self.table).exists():
                raise ValidationError('Time slot already exists for this table')
            else:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)      


class Bookings(models.Model):
    class Meta:
        verbose_name_plural = "Bookings"
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='bookings')
    booking_time = models.TimeField()
    booking_date = models.DateField()
    is_cancelled = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True,blank=True)

