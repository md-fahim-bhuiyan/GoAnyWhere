from django.shortcuts import render
from .models import Destination
from .models import Detailed_desc
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import *
from django import forms
from django.forms.formsets import formset_factory

from datetime import datetime
from django.contrib.auth.models import User
from .models import pessanger_detail
def index(request):
    dests = Destination.objects.all()
    dest1 = []
    j=0
    for i in range(6):
        j=j+2
        temp =Detailed_desc.objects.get(dest_id=j)
        dest1.append(temp)

    return render(request, 'home.html',{'dests': dests, 'dest1' : dest1})


@login_required(login_url='login')
def destination_list(request,city_name):
    dests = Detailed_desc.objects.all().filter(country=city_name)
    return render(request,'travel_destination.html',{'dests': dests})


def destination_details(request,city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request,'destination_details.html',{'dest':dest})

def search(request):
    try:
        place1 = request.session.get('place')
        print(place1)
        dest = Detailed_desc.objects.get(dest_name=place1)
        print(place1)
        return render(request, 'destination_details.html', {'dest': dest})
    except:
        messages.info(request, 'Place not found')
        return redirect('index')

class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
def pessanger_detail_def(request, city_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')
            obj = pessanger_detail.objects.get(Trip_id=3)
            pipo_id = obj.Trip_same_id
            #pipo_id =4
            request.session['Trip_same_id'] = pipo_id
            price = request.session['price']
            city = request.session['city']
            print(request.POST['trip_date'])
            #temp_date = parse_date(request.POST['trip_date'])
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            usernameget = request.user.get_username()
            print(temp_date)
            request.session['n']=formset.total_form_count()
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]

                t = pessanger_detail(Trip_same_id=pipo_id,first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                     age=form.cleaned_data['age'],
                                     Trip_date=temp_date,payment=price,username=usernameget,city=city)
                t.save()
                # print (formset.forms[i].form-[i]-value)

            obj.Trip_same_id = (pipo_id + 1)
            obj.save()
            no_of_person = formset.total_form_count()
            price1 = no_of_person * price
            GST = price1 * 0.18
            GST = float("{:.2f}".format(GST))
            final_total = GST + price1
            request.session['pay_amount'] = final_total
            return render(request,'payment.html', {'no_of_person': no_of_person,
                                                   'price1': price1, 'GST': GST, 'final_total': final_total,'city': city })
    else:
        formset = KeyValueFormSet()

        return render(request, 'sample.html', {'formset': formset, 'city_name': city_name, })


def upcoming_trips(request):
    username = request.user.get_username()
    date1=datetime.now().date()
    person = pessanger_detail.objects.all().filter(username=username).filter(pay_done=1)
    person = person.filter(Trip_date__gte=date1)
    print(date1)
    return render(request,'upcoming trip1.html',{'person':person})