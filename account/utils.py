from datetime import timedelta, datetime
from account.models import *
from .models import Week, Place, Flight
from tqdm import tqdm

def addPlaces():
    for i, line in tqdm(500):
        if i == 0:
            continue
        data = line.split(',')
        city = data[0].strip()
        airport = data[1].strip()
        code = data[2].strip()
        country = data[3].strip()
        Place.objects.create(city=city, airport=airport, code=code, country=country)

def addDomesticFlights():
    file =""
    total =""
    for i, line in tqdm(enumerate(file), total=total):
        if i == 0:
            continue
        data = line.split(',')
        origin = data[1].strip()
        destination = data[2].strip()
        depart_time = datetime.strptime(data[3].strip(), "%H:%M:%S").time()
        depart_week = int(data[4].strip())
        duration = timedelta(hours=int(data[5].strip()[:2]), minutes=int(data[5].strip()[3:5]))
        arrive_time = datetime.strptime(data[6].strip(), "%H:%M:%S").time()
        arrive_week = int(data[7].strip())
        flight_no = data[8].strip()
        airline = data[10].strip()
        economy_fare = float(data[11].strip()) if data[11].strip() else 0.0
        business_fare = float(data[12].strip()) if data[12].strip() else 0.0
        first_fare = float(data[13].strip()) if data[13].strip() else 0.0
        a1 = Flight.objects.create(origin=Place.objects.get(code=origin), destination=Place.objects.get(code=destination), depart_time=depart_time , duration=duration, arrival_time=arrive_time, plane=flight_no, airline=airline, economy_fare=economy_fare, business_fare=business_fare, first_fare=first_fare)
        a1.depart_day.add(Week.objects.get(number=depart_week))
        a1.save()


def addInternationalFlights():
    file ="" 
    total = ""    
    for i, line in tqdm(enumerate(file), total=total):
        if i == 0:
            continue
        data = line.split(',')
        origin = data[1].strip()
        destination = data[2].strip()
        depart_time = datetime.strptime(data[3].strip(), "%H:%M:%S").time()
        depart_week = int(data[4].strip())
        duration = timedelta(hours=int(data[5].strip()[:2]), minutes=int(data[5].strip()[3:5]))
        arrive_time = datetime.strptime(data[6].strip(), "%H:%M:%S").time()
        arrive_week = int(data[7].strip())
        flight_no = data[8].strip()
        airline = data[10].strip()
        economy_fare = float(data[11].strip()) if data[11].strip() else 0.0
        business_fare = float(data[12].strip()) if data[12].strip() else 0.0
        first_fare = float(data[13].strip()) if data[13].strip() else 0.0
        a1 = Flight.objects.create(origin=Place.objects.get(code=origin), destination=Place.objects.get(code=destination), depart_time=depart_time , duration=duration, arrival_time=arrive_time, plane=flight_no, airline=airline, economy_fare=economy_fare, business_fare=business_fare, first_fare=first_fare)
        a1.depart_day.add(Week.objects.get(number=depart_week))
        a1.save()
    print("Done.\n")
