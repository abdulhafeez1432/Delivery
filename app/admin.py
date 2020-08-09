from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(ProfileBike)
admin.site.register(ProfileCustomer)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProcessOrder)
admin.site.register(Order)
admin.site.register(PackageType)
