from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from urllib.request import urlopen


from facebook import *
from core.affected.affected import get_affected_zone

from django.contrib import auth
from django.http import HttpResponseRedirect
import urllib.parse
import urllib

from core.models import Shelter, AssistanceTicket
from disrupt2017 import settings




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
    return render(request, 'blocks/templates/pages/login_page.html', template_context)


def needhelp(request, optional_form=None):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    #result = parse_and_identify(request)
    zone = get_affected_zone(request)
    if zone is not None:
        return render(request, 'victim_form.html')
    else:
        return render(request, 'victim_form.html')
        #return HttpResponse("need to know a bit of location")
    pass

def add_victim(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    #print(key + " = " + request.POST[key])
    print(request.POST.getlist('requirements'))

    return HttpResponse("<h1>Thanks for submitting your information. Here are some guidelines\
        for you</h1>")

def wannahelp(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    return render(request, 'wanna_help.html')

def add_shelter(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    for key in request.POST.keys():
        print(key + ' = ' + request.POST[key])
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