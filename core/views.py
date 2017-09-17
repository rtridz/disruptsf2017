from django.http import HttpResponse
from django.views.generic import TemplateView

from core.models import MyUser, FacebookSession


class indexView(TemplateView):
    template_name = "index.html"

    def index_view(self, *args, **kwargs):
            response = HttpResponse('')
            return response


from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext

import cgi
import simplejson
import urllib
from disrupt2017 import settings


def login(request):
    error = None

    if request.user.is_authenticated():
        return HttpResponseRedirect('/yay/')

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'client_secret': settings.FACEBOOK_API_SECRET,
                'code': request.GET['code'],
            }

            url = 'https://graph.facebook.com/oauth/access_token?' + \
                    urllib.urlencode(args)
            response = cgi.parse_qs(urllib.urlopen(url).read())
            access_token = response['access_token'][0]
            expires = response['expires'][0]

            facebook_session = FacebookSession.objects.get_or_create(
                access_token=access_token,
            )[0]

            facebook_session.expires = expires
            facebook_session.save()

            user = auth.authenticate(token=access_token)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/index')
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