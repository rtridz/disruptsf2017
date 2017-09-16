from django.db import models

# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    location_lat = models.FloatField()
    location_long = models.FloatField()


class Affected(Person):
    shelter_going = models.ForeignKey(Shelter)
    shelter_signed_in = models.ForeignKey(Shelter)


class AssistanceTicket(models.Model):
    user_created = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_created = models.DateField()
    type_of_assistance = models.TextField()

    date_needed = models.DateField()

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
    person_reacted = models.ForeignKey(Person)


class HelpProvider(models.Model):
    orgname = models.CharField(max_length=50)


class Shelter(models.Model):
    provider = models.ForeignKey(HelpProvider, on_delete=models.CASCADE)
    shelter_name = models.CharField(max_length=50)
    location_lat = models.FloatField()
    location_long = models.FloatField()
    address = models.CharField(max_length=100)
    max_capacity = models.IntegerField()
    people_inside = models.IntegerField()
    people_coming = models.IntegerField()


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
    who_demands = models.ForeignKey(Person)
    shelter = models.ForeignKey(Shelter)