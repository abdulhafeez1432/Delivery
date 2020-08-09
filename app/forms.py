from django import forms
from django.db import transaction
from django.forms.utils import ValidationError
from app.models import *
from  django.contrib.auth.forms import  UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, PasswordResetForm
from django.forms import (formset_factory, modelformset_factory)


class CustomerSignUpForm(UserCreationForm):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Username"), error_messages={ 'invalid': ("This value must contain only letters, numbers and underscores.") })
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Surname"))
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("First Name"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password (again)"))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_lenght=50)), label=("Email Address"))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in [ 'username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(("The username already exists. Please try another one."))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # check and raise error if other user already exists with given email
        is_exists = User.objects.filter(email=email).exists()
        if is_exists:
            raise forms.ValidationError("User already exists with this email")
        return email
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("The two password fields did not match."))
        return self.cleaned_data



    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = ProfileCustomer.objects.create(user=user)
        return user


class BikeSignUpForm(UserCreationForm):
   
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Username"), error_messages={ 'invalid': ("This value must contain only letters, numbers and underscores.") })
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Surname"))
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("First Name"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password (again)"))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_lenght=50)), label=("Email Address"))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in [ 'username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("The two password fields did not match."))
        return self.cleaned_data



    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_bike = True
        user.save()
        bike = ProfileBike.objects.create(user=user)
        return user


class CustomerProfileForm(forms.ModelForm):

    
    class Meta:
        model = ProfileCustomer
        exclude = ('updated_at', 'created_at', 'user')


class BikeProfileForm(forms.ModelForm):

    
    class Meta:
        model = ProfileBike
        exclude = ('updated_at', 'created_at', 'user')

class PlaceOrderForm(forms.ModelForm):
    class Meta:
        model = ProcessOrder
        exclude = ['created_at', 'updated_at',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')

SubCategoryFormset = modelformset_factory(
    SubCategory,
    fields=('name', ),
    extra=1,
    
    widgets = {
        'name': forms.Select(attrs={'id': 'subcategory'}),
    }
    
)




class ProcessFoodForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)



class SubCategoryForm(forms.ModelForm):

    INTEGER_CHOICES = [tuple([x,x]) for x in range(1,10)]

    quantity = forms.IntegerField(widget=forms.Select(choices=INTEGER_CHOICES))

    class Meta:
        model = SubCategory
        labels = {"Quantity": "Qty."}
        fields = ('name', 'quantity')

SubCategoryFormset = formset_factory(SubCategoryForm, extra=1)



class OrderCreateForm(forms.ModelForm):
    class Meta: 
        model = Order
        fields = []


class OrderEditForm(forms.ModelForm):
    INTEGER_CHOICES = [tuple([x,x]) for x in range(1,10)]

    quantity = forms.IntegerField(widget=forms.Select(choices=INTEGER_CHOICES))

    class Meta: 
        model = ProcessOrder
        fields = ('subcategory', 'quantity')





class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('shipping_address', 'ordernote', 'package',)


class BikeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('shipping_address', 'ordernote', 'package',)