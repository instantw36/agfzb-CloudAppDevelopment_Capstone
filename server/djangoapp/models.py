from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    other = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    name = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.CharField(max_length=200)

    SEDAN = 'Sedan'
    SUV = 'Suv'
    WAGON = 'Wagon'
    
    CAR_TYPES = [
                (SEDAN, 'Sedan'),
                (SUV, 'Suv'),
                (WAGON, 'Wagon')
                ]
    types = models.CharField(
                            null=False,
                            max_length=20,
                            choices=CAR_TYPES,
                            default=SEDAN
                            )
    types = models.CharField(max_length=20)
    year = models.DateField(default=now)

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer(models.Model)


# <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview(models.Model)


class CarModelInline(models.Model):

    name = models.ForeignKey(CarMake, on_delete=models.CASCADE)