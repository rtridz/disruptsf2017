import requests
from ipware.ip import get_real_ip

def IP2loc(ipaddress):
    response = requests.get('http://ip-api.com/json/' + ipaddress)
    return response

def getIPfromReq(requests):
    return get_reaal_ip(requests)