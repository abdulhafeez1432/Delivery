from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.forms import PasswordChangeForm
from ..decorators import customer_required
from ..forms import *
from ..models import *
from django.contrib.messages.views import SuccessMessageMixin
import random
import string
from decimal import Decimal



def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))




@customer_required
def CustomerDashboard(request):
    return render(request, 'customer/dashboard.html')




class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        p = ProfileCustomer.objects.get(user=self.request.user.id)
        return redirect('customer:customer_profile', p.id)






def CustomerProfile(request, pk):
    template_name = 'customer/editprofile.html'
    customer = get_object_or_404(ProfileCustomer, pk=pk)
    form = CustomerProfileForm(request.POST or None, request.FILES or None, instance = customer)
    if request.method == 'POST':
        if form.is_valid():
            p = form.save(commit=False)
            p.save()
            messages.success(request, "Your Profile Was Updated Successfully...")
            return redirect('customer:dashboard')
    return render(request, template_name, {'form': form})


def load_foodcategory(request):
    category_id = request.GET.get('category')
    subcategory = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'general/order_options.html', {'subcategory': subcategory})








@login_required
def AdCategory(request):
    template_name = 'customer/addcategory.html'
    #form = ProcessFoodForm()
    #form.fields['name'] = forms.ModelChoiceField(Category.objects.all())
    category = Category.objects.all()
    if request.method == 'POST':
        
        form = ProcessFoodForm(request.POST or None)
        if form.is_valid():
            request.session['name'] = request.POST['name']
            #order = request.POST.get('category')
            return redirect('customer:place_order')
           
    return render(request, template_name, {'category': category})




@customer_required
def PlaceOrder(request):
    template_name = 'customer/placeorder.html'
    user = request.user
    orderuser = User.objects.get(id=request.user.id)
    name = request.session.get('name')
    form = SubCategoryFormset()

    if request.method == 'GET':
        for formset in form:
            formset.fields['name'] = forms.ModelChoiceField(SubCategory.objects.filter(category=name))
    
    elif request.method == 'POST':  
        formorder = OrderCreateForm(request.POST)
        formset = SubCategoryFormset(request.POST) 

        if formorder.is_valid() and formset.is_valid():
            order = formorder.save(commit=False)
            order.ref_code = create_ref_code()
            order.user = user
            #order.user = orderuser
            order.save()

                
            for form in formset:
                sub = form.cleaned_data.get('name')
                quantity = form.cleaned_data.get('quantity')
                subcategory = SubCategory.objects.get(id=sub)
                
                if subcategory:
                    ProcessOrder(subcategory=subcategory, order=order, user=user, quantity=quantity).save()
                    
            return redirect('customer:billing', order.id)
            

         
    context = {'form': form}

    
   
    return render(request, template_name, context)

@customer_required
def MyBilling(request, pk):
    template_name = 'customer/order.html'
    order = get_object_or_404(Order, pk=pk, paid=False)  
    item = order.order.all() 
    total_prices = sum((items.subcategory.price * items.quantity) for items in item)
    form = CheckoutForm()
    context = {'form': form, 'order': order, 'total_prices': total_prices,}
    if request.method == 'POST':  
        form = CheckoutForm(request.POST, instance=order)
        if form.is_valid():
            package = form.cleaned_data.get('package')
            shipping_address = form.cleaned_data.get('shipping_address')
            ordernote = form.cleaned_data.get('ordernote')
            pck = PackageType.objects.get(id=package.id)
            grand_total_price = total_prices + pck.price
            order = form.save(commit=False)                
            order.shipping_address = shipping_address
            order.ordernote = ordernote
            order.package = pck
            order.total_price = grand_total_price
            order.save()

            return redirect('customer:payment', order.id)

    return render(request, template_name, context)
        
@customer_required
def PaymentProcess(request, pk):
    order = get_object_or_404(Order, id=pk, paid=False)

    print(order.total_price)
    templates_name = 'customer/payment.html'
    return render(request, templates_name, {'order': order})

 

@customer_required
def SuccessPayment(request, pk):

    order = get_object_or_404(Order, pk=pk)

    Order.objects.filter(pk=order.id).update(paid=True)
    return render(request, 'customer/successpayment.html')

@customer_required
def HistoryOrder(request, pk):
    template_name = 'customer/orderhistory.html'
    order = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, template_name, {'order': order},)


@customer_required
def OrderEdit(request, pk):
    template_name = 'customer/editorder.html'
   

    order = get_object_or_404(Order, pk=pk, paid=False)


    results = order.order.all()

    
    form_list = [OrderEditForm(instance=x, prefix=str(x.id)) for x in results]
    

    if request.method == 'POST':
        form_list = [OrderEditForm(request.POST, instance=x, prefix=str(x.id)) for x in results]
        
        if all(form.is_valid for form in form_list):
            for form in form_list:
                form.save()
            return redirect('customer:payment', order.id)
        else:
            form_list = [OrderEditForm(instance=x, prefix=str(x.id)) for x in order]
    return render(request, template_name, {'form_list':form_list})






@customer_required
def InfoEdit(request,pk):
    template_name = 'customer/editorderinfo.html'
    order = get_object_or_404(Order, pk=pk, paid=False)
    item = order.order.all() 
    total_prices = sum((items.subcategory.price * items.quantity) for items in item)
    #print(total_prices)
    
    form = CheckoutForm(request.POST or None, instance=order)
    if request.method == 'POST':
        if form.is_valid():
            package = form.cleaned_data.get('package')
            pck = PackageType.objects.get(id=package.id)
            p = form.save(commit=False)
            p.total_price  = pck.price + total_prices
            p.save()
            return redirect('customer:payment', order.id)
    return render(request, template_name, {'form': form})