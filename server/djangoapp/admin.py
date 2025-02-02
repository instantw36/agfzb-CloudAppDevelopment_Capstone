from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['make', 'name', 'id', 'type', 'year']
    list_filter = ['type', 'make', 'id', 'year',]
    search_fields = ['make', 'name']
    
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    # inlines = [CarMake, CarModel]
    # search_fields = ['name', 'description']
    inlines = [CarModelInline]
    
    list_display = ('name', 'description')



# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
