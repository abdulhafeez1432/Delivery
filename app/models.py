from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 22.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))



class User(AbstractUser):
    is_bike = models.BooleanField('bikeman status', default=False)
    is_customer = models.BooleanField('Customer status', default=False)







class ProfileCustomer(models.Model):
    
    GENDER = (
        ('Male', "Male"),
        ('Female', "Female"),
    )
    

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField('Phone Number', max_length=25)
    gender = models.CharField('Gender', max_length=10, choices=GENDER)
    address = models.CharField("Permanent Address", max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


class ProfileBike(models.Model):
    
    GENDER = (
        ('Male', "Male"),
        ('Female', "Female"),
    )
    

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField('Phone Number', max_length=25)
    gender = models.CharField('Gender', max_length=10, choices=GENDER)
    address = models.CharField("Permanent Address", max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField("Carteen Name", max_length=50)
    address = models.TextField("Carteen Address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'

    def subcategory(self):
        if not hasattr(self, '_subcategory'):
            self._subcategory = self.subcategory.all()
        return self._subcategory

    class Meta:
       
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):

    category = models.ForeignKey(Category, related_name='subcategory', on_delete=models.CASCADE)
    name = models.CharField("Food Name", max_length=50, help_text="Name of The Food")    
    price = models.DecimalField("Food Price", max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField("Qty.", help_text="Quantity of the food Item you want")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'





   
    
class PackageType(models.Model):
    name = models.CharField("Package Name", max_length=25)
    price = models.DecimalField("Package Price", max_digits=10, decimal_places=2)
    duration = models.DecimalField("Duration Time", max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '{} - {}'.format(self.name, self.price)



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(User, related_name='bike', on_delete=models.CASCADE, blank=True, null=True)
    package = models.ForeignKey(PackageType, related_name='package', on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0000.0)  
    qty = models.PositiveIntegerField(default=1)
    shipping_address = models.CharField("Delivery Address", max_length=150)
    paid = models.BooleanField(default=False)
    ordernote = models.TextField("Order Notes", null=True)
    shipped = models.BooleanField(default=False)
    complete = models.BooleanField(default=False) 
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.id)


    def order(self):
        if not hasattr(self, '_order'):
            self._order = self.order.all()
        return self._order

    

    
    

    def get_total_cost(self):
        total_cost = sum((items.subcategory.price * items.quantity) for items in self.order.all())
        return total_cost

    def get_grant_total(self):
        #total_cost = sum((items.subcategory.price * items.quantity) for items in self.order.all())
        grand_total = self.package.price + self.get_total_cost()
        return grand_total 


    def get_package(self):
        order_package = f'{self.package.name} {self.package.price}'
        return order_package 

    


class ProcessOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Qty.", default=1, help_text="Quantity of the food Item you want")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_price_cost(self):
        good_price = self.subcategory.price
        return good_price

    def get_good_name(self):
        good_name = self.subcategory.name
        return good_name

    


    def __str__(self):
        return f'{self.order} -- {self.subcategory.name}'

