import urllib

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.db import models
from django.contrib.auth.models import User
import json

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password, facebook_id, link, name, gender, username):
        """
        Creates and saves a User with the given email, date of
        birth,password, facebook id, link, name,gender and balance.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            date_of_birth=date_of_birth,
            facebook_id=facebook_id,
            link=link,
            name=name,
            gender=gender,
            username=username,
        )

        user.set_password(password)
        user.is_admin = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password)

        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    facebook_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=300, null=True)
    link = models.URLField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=300, blank=True)
    gender = models.CharField(max_length=200, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    def get_balance(self):
        return self.balance

    def get_gender(self):
        return self.gender

    def get_link(self):
        return self.link

    def get_username(self):
        return self.username

    def get_birthday(self):
        return self.date_of_birth

    def get_name(self):
        return self.name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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

#
# def get_addr_from_cord(lat,long):
#     url = 'https://www.mapquestapi.com/geocoding/v1/reverse?key=KEY&location=%s-%s&outFormat=json&thumbMaps=false' % (lat,long)
#
#     webURL = urllib.request.urlopen(url)
#     data = webURL.read()
#     encoding = webURL.info().get_content_charset('utf-8')
#     response = json.loads(data.decode(encoding))
#     print(response)
#     return


class Shelter(models.Model):
    shelter_name = models.CharField(max_length=50)
    location_lat = models.FloatField()
    location_long = models.FloatField()
    max_capacity = models.IntegerField()
    people_inside = models.IntegerField()
    people_coming = models.IntegerField()
    # address = models.CharField(max_length=200)


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
