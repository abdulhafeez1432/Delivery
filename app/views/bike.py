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
from ..decorators import bike_required
from ..forms import *
from ..models import *
from django.contrib.messages.views import SuccessMessageMixin





@bike_required
def BikeDashboard(request):
    return render(request, 'bike/dashboard.html')




class BikeSignUpView(CreateView):
    model = User
    form_class = BikeSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'bikeman'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        p = ProfileBike.objects.get(user=self.request.user.id)
        return redirect('bike:bike_profile', p.id)


def BikeProfile(request, pk):
    template_name = 'bike/bikeprofile.html'
    bike = get_object_or_404(ProfileBike, pk=pk)
    form = BikeProfileForm(request.POST or None, request.FILES or None, instance = bike)
    if request.method == 'POST':
        if form.is_valid():
            p = form.save(commit=False)
            p.save()
            return redirect('bike:dashboard')
    return render(request, template_name, {'form': form})


def DeliveryOrder(request):
    template_name = 'bike/orderhistory.html'
    order = Order.objects.filter(received=False, paid=True).order_by('-created_at')

    
    
    return render(request, template_name, {'order': order})

def DetailsOrder(request, pk):
    template_name = 'bike/orders.html'
    orders = get_object_or_404(Order, pk=pk)
    neworder = orders.id
    order = ProcessOrder.objects.filter(order=orders).first()
    if request.method == 'POST':
       
        p = Order.objects.filter(id=neworder).update(received=True)
        return redirect('bike:accept_order', orders.id)

    return render(request, template_name, {'orders': orders, 'order': order})


def AcceptOrder(request, pk):
    template_name = 'bike/accept.html'
    orders = get_object_or_404(Order, pk=pk)
    neworder = orders.id
    order = ProcessOrder.objects.filter(order=orders).first()
    if request.method == 'POST':
        p = Order.objects.filter(id=neworder).update(shipped=True)
        return redirect('bike:complete_order', orders.id)
    return render(request, template_name, {'orders': orders, 'order': order})


def CompleteOrder(request, pk):
    template_name = 'bike/completed.html'
    orders = get_object_or_404(Order, pk=pk)
    neworder = orders.id
    order = ProcessOrder.objects.filter(order=orders).first()
    if request.method == 'POST':
        p = Order.objects.filter(id=neworder).update(complete=True)
        return redirect('bike:order_delivery')
    return render(request, template_name, {'orders': orders, 'order': order})