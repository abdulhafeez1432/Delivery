from django.urls import include, path
from .views import general, customer, bike

urlpatterns = [
    path('home/', general.home, name='home'),
    path('', general.FrontPage, name='front_page'),
    
    path('logout', general.logout_user, name='user_logout'),
    path("login", general.login, name='userlogin'),


    path('bike/', include(([

        path('dashboard', bike.BikeDashboard, name='dashboard'),
        path('profile/<pk>', bike.BikeProfile, name='bike_profile'),
        path('orders', bike.DeliveryOrder, name='order_delivery'),
        path('ordersdetails/<pk>', bike.DetailsOrder, name='details'),
        path('orderaccept/<pk>', bike.AcceptOrder, name='accept_order'),
        path('ordercompleted/<pk>', bike.CompleteOrder, name='complete_order'),


   
      
    ], 'app'), namespace='bike')),

    path('customer/', include(([

        path('dashboard', customer.CustomerDashboard, name='dashboard'),
        path('profile/<pk>', customer.CustomerProfile, name='customer_profile'),
        path('order', customer.PlaceOrder, name='place_order'),
        path('ajax/load-subcategories/', customer.load_foodcategory, name='ajax_load_subcategories'),
        path('category', customer.AdCategory, name='category'),
        path('billing/<pk>', customer.MyBilling, name='billing'),
        path('payment/<pk>', customer.PaymentProcess, name='payment'),
        path('done/<pk>', customer.SuccessPayment, name='successpayment'),
        path('history/<pk>', customer.HistoryOrder, name='order_history'),
        path('edit/<pk>', customer.OrderEdit, name='order_edit'),
        path('info/<pk>', customer.InfoEdit, name='info_edit'),
        


        
       
       
    ], 'app'), namespace='customer')),
]