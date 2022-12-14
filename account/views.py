from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationserializer
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.models import auth
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import math
from django.urls import reverse
from .models import *
from GoAnywhere.utils import render_to_pdf, createticket
from .constant import FEE
from django.contrib.auth.decorators import login_required
from .forms import Contact, PlaceF, HotelF,RoomF,FlightF

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def home(request):
    data = {
        'current_year': datetime.now().year
    }
    return render(request, 'home.html', data)


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return redirect('login')
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


def register(request):
    return render(request, 'registation.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Sucessfully Logged in')
            email = request.user.email
            print(email)
            return redirect('home')
        else:
            return render(request, "login.html", {
                "message": "Invalid Email and/or password."
            })
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def index(request):
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        depart_date = request.POST.get('DepartDate')
        seat = request.POST.get('SeatClass')
        trip_type = request.POST.get('TripType')
        if (trip_type == '1'):
            return render(request, 'flight/index.html', {
                'origin': origin,
                'destination': destination,
                'depart_date': depart_date,
                'seat': seat.lower(),
                'trip_type': trip_type
            })
        elif (trip_type == '2'):
            return_date = request.POST.get('ReturnDate')
            return render(request, 'flight/index.html', {
                'min_date': min_date,
                'max_date': max_date,
                'origin': origin,
                'destination': destination,
                'depart_date': depart_date,
                'seat': seat.lower(),
                'trip_type': trip_type,
                'return_date': return_date
            })
    else:
        return render(request, 'flight/index.html', {
            'min_date': min_date,
            'max_date': max_date
        })


@login_required
def profile(request):
    return render(request, 'profile.html')


def resetPassword(request):

    return render(request, 'resetPassword.html')


def query(request, q):
    places = Place.objects.all()
    filters = []
    q = q.lower()
    for place in places:
        if (q in place.city.lower()) or (q in place.airport.lower()) or (q in place.code.lower()) or (q in place.country.lower()):
            filters.append(place)
    return JsonResponse([{'code': place.code, 'city': place.city, 'country': place.country} for place in filters], safe=False)


@csrf_exempt
def flight(request):
    o_place = request.GET.get('Origin')
    d_place = request.GET.get('Destination')
    trip_type = request.GET.get('TripType')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    return_date = None
    if trip_type == '2':
        returndate = request.GET.get('ReturnDate')
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        flightday2 = Week.objects.get(number=return_date.weekday()) 
        origin2 = Place.objects.get(code=d_place.upper())   
        destination2 = Place.objects.get(code=o_place.upper())  
    seat = request.GET.get('SeatClass')

    flightday = Week.objects.get(number=depart_date.weekday())
    destination = Place.objects.get(code=d_place.upper())
    origin = Place.objects.get(code=o_place.upper())
    if seat == 'economy':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(economy_fare=0).order_by('economy_fare')
        try:
            max_price = flights.last().economy_fare
            min_price = flights.first().economy_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(economy_fare=0).order_by('economy_fare')    ##
            try:
                max_price2 = flights2.last().economy_fare   
                min_price2 = flights2.first().economy_fare  
            except:
                max_price2 = 0  
                min_price2 = 0  
                
    elif seat == 'business':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(business_fare=0).order_by('business_fare')
        try:
            max_price = flights.last().business_fare
            min_price = flights.first().business_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(business_fare=0).order_by('business_fare')    ##
            try:
                max_price2 = flights2.last().business_fare   
                min_price2 = flights2.first().business_fare  
            except:
                max_price2 = 0  
                min_price2 = 0  

    elif seat == 'first':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(first_fare=0).order_by('first_fare')
        try:
            max_price = flights.last().first_fare
            min_price = flights.first().first_fare
        except:
            max_price = 0
            min_price = 0
            
        if trip_type == '2':    
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(first_fare=0).order_by('first_fare')
            try:
                max_price2 = flights2.last().first_fare   
                min_price2 = flights2.first().first_fare  
            except:
                max_price2 = 0  
                min_price2 = 0      

    if trip_type == '2':
        return render(request, "flight/search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'flights2': flights2,   
            'origin2': origin2,    
            'destination2': destination2,    
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100,
            'max_price2': math.ceil(max_price2/100)*100,    
            'min_price2': math.floor(min_price2/100)*100    
        })
    else:
        return render(request, "flight/search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100
        })


def review(request):
    flight_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    seat = request.GET.get('seatClass')
    round_trip = False
    if request.GET.get('flight2Id'):
        round_trip = True

    if round_trip:
        flight_2 = request.GET.get('flight2Id')
        date2 = request.GET.get('flight2Date')

    if request.user.is_authenticated:
        flight1 = Flight.objects.get(id=flight_1)
        flight1ddate = datetime(int(date1.split('-')[2]), int(date1.split('-')[1]), int(
            date1.split('-')[0]), flight1.depart_time.hour, flight1.depart_time.minute)
        flight1adate = (flight1ddate + flight1.duration)
        flight2 = None
        flight2ddate = None
        flight2adate = None
        if round_trip:
            flight2 = Flight.objects.get(id=flight_2)
            flight2ddate = datetime(int(date2.split('-')[2]), int(date2.split('-')[1]), int(
                date2.split('-')[0]), flight2.depart_time.hour, flight2.depart_time.minute)
            flight2adate = (flight2ddate + flight2.duration)
        if round_trip:
            return render(request, "flight/book.html", {
                'flight1': flight1,
                'flight2': flight2,
                "flight1ddate": flight1ddate,
                "flight1adate": flight1adate,
                "flight2ddate": flight2ddate,
                "flight2adate": flight2adate,
                "seat": seat,
                "fee": FEE
            })
        return render(request, "flight/book.html", {
            'flight1': flight1,
            "flight1ddate": flight1ddate,
            "flight1adate": flight1adate,
            "seat": seat,
            "fee": FEE
        })
    else:
        return HttpResponseRedirect(reverse("login"))


def book(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            flight_1 = request.POST.get('flight1')
            flight_1date = request.POST.get('flight1Date')
            flight_1class = request.POST.get('flight1Class')
            f2 = False
            if request.POST.get('flight2'):
                flight_2 = request.POST.get('flight2')
                flight_2date = request.POST.get('flight2Date')
                flight_2class = request.POST.get('flight2Class')
                f2 = True
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            flight1 = Flight.objects.get(id=flight_1)
            if f2:
                flight2 = Flight.objects.get(id=flight_2)
            passengerscount = request.POST['passengersCount']
            passengers = []
            for i in range(1, int(passengerscount)+1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(
                    first_name=fname, last_name=lname, gender=gender.lower()))
            coupon = request.POST.get('coupon')

            try:
                ticket1 = createticket(request.user, passengers, passengerscount, flight1,
                                       flight_1date, flight_1class, coupon, countrycode, email, mobile)
                if f2:
                    ticket2 = createticket(request.user, passengers, passengerscount, flight2,
                                           flight_2date, flight_2class, coupon, countrycode, email, mobile)

                if (flight_1class == 'Economy'):
                    if f2:
                        fare = (flight1.economy_fare*int(passengerscount)) + \
                            (flight2.economy_fare*int(passengerscount))
                    else:
                        fare = flight1.economy_fare*int(passengerscount)
                elif (flight_1class == 'Business'):
                    if f2:
                        fare = (flight1.business_fare*int(passengerscount)) + \
                            (flight2.business_fare*int(passengerscount))
                    else:
                        fare = flight1.business_fare*int(passengerscount)
                elif (flight_1class == 'First'):
                    if f2:
                        fare = (flight1.first_fare*int(passengerscount)) + \
                            (flight2.first_fare*int(passengerscount))
                    else:
                        fare = flight1.first_fare*int(passengerscount)
            except Exception as e:
                return HttpResponse(e)

            if f2:
                return render(request, "flight/payment.html", {
                    'fare': fare+FEE,
                    'ticket': ticket1.id,
                    'ticket2': ticket2.id
                })
            return render(request, "flight/payment.html", {
                'fare': fare+FEE,
                'ticket': ticket1.id
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")


def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket_id = request.POST['ticket']
            t2 = False
            if request.POST.get('ticket2'):
                ticket2_id = request.POST['ticket2']
                t2 = True
            fare = request.POST.get('fare')
            card_number = request.POST['cardNumber']
            card_holder_name = request.POST['cardHolderName']
            exp_month = request.POST['expMonth']
            exp_year = request.POST['expYear']
            cvv = request.POST['cvv']
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.status = 'CONFIRMED'
            ticket.booking_date = datetime.now()
            ticket.save()
            if t2:
                ticket2 = Ticket.objects.get(id=ticket2_id)
                ticket2.status = 'CONFIRMED'
                ticket2.save()
                return render(request, 'flight/payment_process.html', {
                    'ticket1': ticket,
                    'ticket2': ticket2
                })
            return render(request, 'flight/payment_process.html', {
                'ticket1': ticket,
                'ticket2': ""
            })
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login'))


def ticket_data(request, ref):
    ticket = Ticket.objects.get(ref_no=ref)
    return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.flight.origin.code,
        'to': ticket.flight.destination.code,
        'flight_date': ticket.flight_ddate,
        'status': ticket.status
    })

@csrf_exempt
def get_ticket(request):
    ref = request.GET.get("ref")
    ticket1 = Ticket.objects.get(ref_no=ref)
    data = {
        'ticket1': ticket1,
        'current_year': datetime.now().year
    }
    pdf = render_to_pdf('flight/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def bookings(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(
            user=request.user).order_by('-booking_date')
        return render(request, 'flight/bookings.html', {
            'page': 'bookings',
            'tickets': tickets
        })
    else:
        return HttpResponseRedirect(reverse('login'))

def hotel(request):
    all_location = Hotel.objects.values_list(
        'location', 'id').distinct().order_by()
    if request.method == "POST":
        try:
            print(request.POST)
            hotel = Hotel.objects.all().get(
                id=int(request.POST['search_location']))
            rr = []
            for each_reservation in Reservation.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.room.id)
            room = Room.objects.all().filter(hotel=hotel, capacity__gte=int(
                request.POST['capacity'])).exclude(id__in=rr)
            if len(room) == 0:
                messages.warning(
                    request, "Sorry No Rooms Are Available on this time period")
            data = {'rooms': room, 'all_location': all_location, 'flag': True}
            response = render(request, 'hotel/index.html', data)
        except Exception as e:
            messages.error(request, e)
            response = render(request, 'hotel/index.html',
                              {'all_location': all_location})
    else:
        data = {'all_location': all_location}
        response = render(request, 'hotel/index.html', data)
    return HttpResponse(response)


@login_required(login_url='/user')
def book_room_page(request):
    room = Room.objects.all().get(id=int(request.GET['roomid']))
    return HttpResponse(render(request, 'hotel/bookroom.html', {'room': room}))


@login_required(login_url='/user')
def book_room(request):
    if request.method == "POST":
        room_id = request.POST['room_id']
        room = Room.objects.all().get(id=room_id)
        for each_reservation in Reservation.objects.all().filter(room=room):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(
                    request, "Sorry This Room is unavailable for Booking")
                return redirect("hotel")

        current_user = request.user
        total_person = int(request.POST['person'])
        # booking_id = str(room_id) + str(datetime.datetime.now())
        reservation = Reservation()
        room_object = Room.objects.all().get(id=room_id)
        room_object.status = '2'
        user_object = User.objects.all().get(email=current_user)
        reservation.guest = user_object
        reservation.room = room_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']
        reservation.save()
        messages.success(request, "Congratulations! Booking Successfull")
        return redirect("hotel")
    else:
        return HttpResponse('Access Denied')


def contact(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    form = Contact()
    context = {'form': form}
    return render(request, 'contact.html', context)


def place(request):
    if request.method == 'POST':
        form = PlaceF(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    form = PlaceF()
    context = {'form': form}
    return render(request, 'flight/addplace.html', context)


@login_required
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(guest=user)
    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'hotel/mybookings.html',{'bookings':bookings}))

def addhotel(request):
    if request.method == 'POST':
        form = HotelF(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    form = HotelF()
    context = {'form': form}
    return render(request, 'hotel/addhotel.html', context)

    
def addroom(request):
    hotel_name = Hotel.objects.values_list('name', 'id').distinct().order_by()
    data = {'hotel_name': hotel_name}
    return render(request, 'hotel/addroom.html',data)

def addrooms(request):
    if request.method == 'POST':
        form = RoomF(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')

                                 
def addflight(request):
    airport_name = Place.objects.values_list('airport', 'id').distinct().order_by()
    day_name = Week.objects.values_list('name', 'id').distinct().order_by()
    data = {
        'airport_name': airport_name,
        'day_name': day_name
        }
    return render(request, 'flight/addflight.html',data)

def addflights(request):
    if request.method == 'POST':
        form = FlightF(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')


def privacy_policy(request):
    return render(request, 'privacy-policy.html')


def terms_and_conditions(request):
    return render(request, 'terms.html')


def aboutus(request):
    return render(request, 'about.html')