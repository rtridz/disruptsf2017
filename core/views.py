from urllib.request import urlopen
from django.http import HttpResponse


from facebook import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from core import models
from core.affected.affected import get_affected_zone
from core.models import MyUser

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
import urllib.parse
import urllib
from disrupt2017 import settings




def index_view(request):
    error = None

    template_context = {'settings': settings, 'error': error}

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

            print(response)

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
    return render(request, 'blocks/facebook.html', template_context)



def needhelp(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    #result = parse_and_identify(request)
    zone = get_affected_zone(request)
    if zone is not None:
        return optional_form
    else:
        return HttpResponse("need to know a bit of location")
    pass

def wannahelp(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    pass

def operator(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    pass

def viewer(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    pass

