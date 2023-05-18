from django.db import models
from django.utils.timezone import now
import uuid
import json
import datetime


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='')
    description = models.CharField(max_length=200)
    # other = models.CharField(max_length=200)

    def __str__(self):
        return "Name: " + self.name# + "," + "Description: " + self.description

def current_year():
    return datetime.date.today().year

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.IntegerField(default=1,primary_key=True)
    name = models.CharField(null=False, max_length=100, default='Car')
   
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    MINIVAN = 'Minivan'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (MINIVAN, 'Minivan')
    ]

    type = models.CharField(
        null=False,
        max_length=50,
        choices=CAR_TYPES,
        default=SEDAN
    )
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# # <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review,):
        self.make = ""
        self.car_model = ""
        self.car_year = ""
        self.dealership = dealership
        self.id = ""  # The id of the review
        self.name = name  # Name of the reviewer
        self.purchase = purchase  # Did the reviewer purchase the car? bool
        self.purchase_date = ""
        self.review = review  # The actual review text
        self.sentiment = ""  # Watson NLU sentiment analysis of review

    def __str__(self):
        return "Reviewer: " + self.name + " Review: " + self.review

# # <HINT> Create a plain Python class `ReviewPost` to post review data
class ReviewPost:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)