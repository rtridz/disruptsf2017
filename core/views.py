from django.http import HttpResponse
from django.shortcuts import render
from affected.affected import *
from utilities import *
#from urllib.request import urlopen
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic import TemplateView
#from facebook import *
from django.contrib.auth import authenticate
import datetime
from config import conf
from core.models import MyUser

class indexView(TemplateView):
    template_name = "index.html"

    def index_view(self, *args, **kwargs):
            response = HttpResponse('')
            return response


'''
def facebookReturn(request):
    code = request.GET.get('code')

    site=urlopen("https://graph.facebook.com/oauth/access_token?client_id=" + str(conf.facevook_id) + "&redirect_uri=http://localhost:8000/facebookreturn&client_secret=" + str(conf.facevook_id) + "&code=%s#_=_" % code)

    site = site.replace("access_token=", '')
    m = site.find('&expires=')
    site = site[0:m]

    ##this is the API call that uses the facebook module to get the user data
    graph = GraphAPI(site)
    profile = graph.get_object("me")
    facebook_id = profile.get('id')
    username = profile.get('username')
    email = profile.get('email')
    name = profile.get('name')
    birthday = profile.get('birthday')
    birthday = datetime.datetime.strptime(birthday, '%m/%d/%Y').strftime('%Y-%m-%d')
    gender = profile.get('gender')
    link = profile.get('link')
    try:
        ##this checks if the user is registered on the system, if so it authenticates the user, if not it creates the user
        user = MyUser.objects.get(email=email)
        user = authenticate(username=email, password=facebook_id)
        return HttpResponse('this users email address is %s' % user)
    except ObjectDoesNotExist:
        New_user = MyUser.objects.create_user(email=email, date_of_birth=birthday, password=facebook_id,
                                              facebook_id=facebook_id, link=link, name=name, gender=gender,
                                              username=username)
        return HttpResponse(
            "facebook id %s\n, username %s\n, email %s\n, name %s\n, birthday %s\n, gender %s\n, link %s" % (
            facebook_id, username, email, name, birthday, gender, link))
'''
def needhelp(request):
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