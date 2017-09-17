from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin

from django.db import models
from django.contrib.auth.models import User
import json
import urllib.parse


class MyUser(AbstractUser):
    phone_number = models.CharField(max_length=103, blank=True, null=True)
    facebook_id = models.BigIntegerField(blank=True, null=True)


class FacebookSessionError(Exception):
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type

    def get_message(self):
        return self.message

    def get_type(self):
        return self.type

    def __unicode__(self):
        return u'%s: "%s"' % (self.type, self.message)

class FacebookSession(models.Model):

    access_token = models.CharField(max_length=103, unique=True)
    expires = models.IntegerField(null=True)

    user = models.ForeignKey(MyUser, null=True)
    uid = models.BigIntegerField(unique=True, null=True)

    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))

    def query(self, object_id, connection_type=None, metadata=False):

        url = 'https://graph.facebook.com/%s' % (object_id)
        if connection_type:
            url += '/%s' % (connection_type)

        params = {'access_token': self.access_token}
        if metadata:
            params['metadata'] = 1

        url += '?' + urllib.parse.urlencode(params)
        webURL = urllib.request.urlopen(url)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        response = json.loads(data.decode(encoding))


        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])
        return response

#
# class Person(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     date_of_birth = models.DateField()
#     email = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=50)
#     location_lat = models.FloatField()
#     location_long = models.FloatField()
#
#

class HelpProvider(models.Model):
    orgname = models.CharField(max_length=50)


class Shelter(models.Model):
    shelter_name = models.CharField(max_length=50)
    location_lat = models.FloatField()
    location_long = models.FloatField()
    max_capacity = models.IntegerField()
    people_inside = models.IntegerField()
    people_coming = models.IntegerField()


class ShelterTicket(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    family_size = models.IntegerField(blank=True, null=True)

    GOING_TO = 1
    SIGNED_IN = 2
    TYPE_CHOICES = (
        (GOING_TO, 'Going to'),
        (SIGNED_IN, 'Signed in'),
    )
    connection_type = models.IntegerField(choices=TYPE_CHOICES) 


class AssistanceTicket(models.Model):
    #user_created = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    #date_created = models.DateField()
    #date_needed = models.DateField()
    phone_number = models.CharField(max_length=11)
    date_created = models.DateField(auto_now_add=True)
    date_needed = models.DateField(auto_now_add=True)
    type_of_assistance = models.TextField()
    location_lat = models.FloatField()
    location_long = models.FloatField()
    selected = models.BooleanField(default=False)

    CRITICAL = 1
    URGENT = 2
    NORMAL = 3
    DESIRABLE = 4
    STATUS_CHOICES = (
        (CRITICAL, 'Critical'),
        (URGENT, 'Urgent'),
        (NORMAL, 'Normal'),
        (DESIRABLE, 'Desirable')
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=NORMAL)


class AssistanceTicketReaction(models.Model):
    ticket = models.ForeignKey(AssistanceTicket)
    person_reacted = models.ForeignKey(MyUser)


class GoodsDemands(models.Model):
    FOOD = 1
    WATER = 2
    BLANKET = 3
    PAIN_KILLER = 4
    SEDATIVE = 5
    GOODS_TYPES = (
        (FOOD, 'food pack'),
        (WATER, 'water pack (2l)'),
        (BLANKET, 'blanket'),
        (PAIN_KILLER, 'pain killer'),
        (SEDATIVE, "sedative")
    )
    good_type = models.IntegerField(choices=GOODS_TYPES)
    qty = models.IntegerField()
    who_demands = models.ForeignKey(MyUser)
    shelter = models.ForeignKey(Shelter)


# ============Managers===============
# class PersonManager(models.Manager):
#     def get_by_natural_key(self, first_name, last_name):
#         return self.get(first_name=first_name, last_name=last_name)

#
# class ShelterManager(models.Manager):
#     def get_by_natural_key(self, provider, shelter_name):
#         return self.get(provider=provider, shelter_name=shelter_name)
