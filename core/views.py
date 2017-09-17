import urllib

from django.http import HttpResponse
from django.shortcuts import render
from core.models import *

from facebook import *
from core.affected.affected import get_affected_zone

from django.contrib import auth
from django.http import HttpResponseRedirect
from core.models import Shelter, AssistanceTicket
from disrupt2017 import settings
import json


def indexView(request):
    error = None

    template_context = {'settings': settings, 'error': error,
                        'shelters': Shelter.objects.all(),
                        'tickets': AssistanceTicket.objects.all()
                        }

    return render(request, 'index.html', template_context)


def login(request):
    error = None

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'client_secret': settings.FACEBOOK_API_SECRET,
                'code': request.GET['code'],
            }


            url = 'https://graph.facebook.com/oauth/access_token?' + urllib.parse.urlencode(args)
            webURL = urllib.request.urlopen(url)
            data = webURL.read()
            encoding = webURL.info().get_content_charset('utf-8')
            response=json.loads(data.decode(encoding))

            access_token = response['access_token']
            expires = response['expires_in']


            user = auth.authenticate(token=access_token, expires=expires)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        elif 'error_reason' in request.GET:
            error = 'AUTH_DENIED'

    template_context = {'settings': settings, 'error': error}
    return render(request, 'pages/login_page.html', template_context)


def needhelp(request, optional_form=None):
    """Summary

    Args:
        request (TYPE): Description
    """
    #result = parse_and_identify(request)


    zone = get_affected_zone(request)
    # if zone is not None:
    return render(request, 'victim_form.html', 
                  {'shelter_id': request.GET['shelter_id']})
    # else:
    #     return render(request, 'victim_form.html')
        #return HttpResponse("need to know a bit of location")


def add_victim(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    #print(key + " = " + request.POST[key])
    if request.POST:
        user = MyUser.objects.create(
            username=request.POST['name'],
            password=request.POST['password'],
            phone_number=request.POST['phone'],
            email=request.POST['email'])
        user.save()

        shelter_ticket = ShelterTicket.objects.create(
            user=user,
            shelter=Shelter.objects.get(pk=int(request.POST['shelter_id'])),
            connection_type=1)
        shelter_ticket.save()

        user = auth.authenticate(username=request.POST['name'], 
                            password=request.POST['password'])
        if user:
            auth.login(request, user)

    return HttpResponse("<h1>Thanks for submitting your information. Here are some guidelines\
        for you</h1>")

def wannahelp(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    return render(request, 'wanna_help_1.html')

def add_shelter(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    #Get provider
    for key in request.POST.keys():
        print(key + ' = ' + request.POST[key])
    #url = 'http://open.mapquestapi.com/nominatim/v1/search.php?key=gowXM2f6C16NEmCvkFMehr5gpfnAjDPI&format=json&q='
    #query = '+'.join(request.POST['address'].split())
    #response = requests.get(url+query)
    #resp = ast.literal_eval(response.text)
    shelter = Shelter(shelter_name=request.POST['name'],\
        location_lat=request.POST['lat'], location_long=request.POST['long'],\
        max_capacity=request.POST['capacity'], people_inside=request.POST['inside']\
        ,people_coming=request.POST['incoming'])
    #return HttpResponse(response)
    return HttpResponse("<h1>Thanks for submitting your information. Gotta need stuff there</h1>")


def operator(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    return

def viewer(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    pass

def emergency_help(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    query = AssistanceTicket()
    query.phone_number = request.POST['number']
    query.type_of_assistance = request.POST['type']
    query.location_lat = request.POST['lat']
    query.location_long = request.POST['long']
    query.status = request.POST['status']
    query.save()
    return HttpResponse("Your request has been registered will be receiving help very soon")

def get_tickets(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    tickets = list(AssistanceTicket.objects.get())
    #for ticket in tickets:
    data = json.dumps(tickets)
    return HttpResponse(data, content_type='application/json')
