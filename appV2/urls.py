from .views import *
from django.urls import path, include
from knox import views as knox_views

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Kwiky API Details')
from rest_framework.documentation import include_docs_urls









urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='reset_password')),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/updatecustomer/<pk>/', ProfileUpdateAPIView.as_view(), name='update_customer'),
    path('api/category/', category_view, name='category_view'),
    path('api/category/<int:category_id>/', category_detail_view, name='category_detail_view'),
    path('api/<int:category_id>/subcategory/', subcategory_view, name='category_view'),
    path('api/processorder/order/', processorder_view, name='processorder_view'),
    
    path('api/myorderdetails/<int:order_id>', order_detail_view, name='my_order'),
    
    path('api/proceedorder/<int:order_id>', proceed_order_view, name='proceed_order'),

    #path('api/myproceedorder/<int:order_id>', proceed_order_view, name='proceed_order'),
    
    path('api/billing/<int:order_id>', billing_order_view, name='billing_order'),


    path(r'api/swagger-docs/', schema_view),
    path(r'docs/', include_docs_urls(title='kwiky Delivery API')),




    #path('questions/', apiviews.questions_view, name='questions_view'),




    

    

] 