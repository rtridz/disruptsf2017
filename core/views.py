from django.http import HttpResponse
from django.shortcuts import render
from affected.affected import *
from utilities import *

# Create your views here.
def home(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    pass

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