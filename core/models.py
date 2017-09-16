from django.db import models

# Create your models here.

class Affected(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    location_lat = models.FloatField()
    location_long = models.FloatField()


class HelpTicket(models.Model):
    user_created = models.ForeignKey(Affected, on_delete=models.CASCADE)
    date_created = models.DateField()
    type_of_assistance = models.TextField()
    level_of_urgency = models.IntegerField()
    date_needed = models.DateField()


class HelpProvider(models.Model):
    orgname = models.CharField(max_length=50)


class Shelter(models.Model):
    provider = models.ForeignKey(HelpProvider, on_delete=models.CASCADE)
    location_lat = models.FloatField()
    location_long = models.FloatField()
    