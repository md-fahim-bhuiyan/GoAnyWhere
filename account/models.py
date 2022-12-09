from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None, password2=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    class Meta:
        db_table = "UserManager"


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    class Meta:
        db_table = "User"


class Place(models.Model):
    city = models.CharField(max_length=64)
    airport = models.CharField(max_length=64)
    code = models.CharField(max_length=3)
    country = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.code})"

    class Meta:
        db_table='Place'

class Week(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} ({self.number})"
    class Meta:
        db_table='Week'


class Flight(models.Model):
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="arrivals")
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    depart_day = models.ManyToManyField(Week, related_name="flights_of_the_day")
    duration = models.DurationField(null=True)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    plane = models.CharField(max_length=24)
    airline = models.CharField(max_length=64)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
    class Meta:
        db_table='Flight'


GENDER = (
    ('male', 'MALE'),
    ('female', 'FEMALE')
)


class Passenger(models.Model):
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=True)

    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name}, {self.gender}"
    class Meta:
        db_table='Passenger'

SEAT_CLASS = (
    ('economy', 'Economy'),
    ('business', 'Business'),
    ('first', 'First')
)

TICKET_STATUS = (
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled')
)




class Ticket(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings", blank=True, null=True)
    ref_no = models.CharField(max_length=6, unique=True)
    passengers = models.ManyToManyField(
        Passenger, related_name="flight_tickets")
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    flight_ddate = models.DateField(blank=True, null=True)
    flight_adate = models.DateField(blank=True, null=True)
    flight_fare = models.FloatField(blank=True, null=True)
    other_charges = models.FloatField(blank=True, null=True)
    coupon_used = models.CharField(max_length=15, blank=True)
    coupon_discount = models.FloatField(default=0.0)
    total_fare = models.FloatField(blank=True, null=True)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=datetime.now)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)

    def __str__(self):
        return self.ref_no
    class Meta:
        db_table='Ticket'


class Hotel(models.Model):
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        db_table='Hotel'


class Room(models.Model):
    ROOM_STATUS = (
        ("1", "Available"),
        ("2", "Not Available"),
    )

    ROOM_TYPE = (
        ("1", "Premium"),
        ("2", "Deluxe"),
        ("3", "Basic"),
    )

    room_type = models.CharField(max_length=50, choices=ROOM_TYPE)
    capacity = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    status = models.CharField(choices=ROOM_STATUS, max_length=15)
    roomnumber = models.IntegerField()

    def __str__(self):
        return self.hotel.name
    class Meta:
        db_table='Room'


class Reservation(models.Model):
    check_in = models.DateField(auto_now=False)
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, default="null")

    def __str__(self):
        return self.guest.email
    class Meta:
        db_table='Reservation'


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        db_table='Contact'
