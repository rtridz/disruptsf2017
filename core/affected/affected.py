from .. import utilities

def parse_and_identify(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    result = {}
    if 'lat' in request.POST.keys() and 'long' in request.POST.keys():
        #append values to result here
        result['lat'] = request.POST['lat']
        result['long'] = request.POST['long']
    else:
        result = {"status":"Invalid request"}
        return result
    return result

def get_affected_zone(request):
    """Summary
    
    Args:
        request (TYPE): Description
    """
    ip = utilities.getIPfromReq(request)
    if ip is not None:
        location = IP2loc(ip)
    else:
        return None