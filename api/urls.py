from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from api.views import *

urlpatterns = [
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    #re_path('api/(?P<version>(v1|v2))/', include('music.urls'))
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    path('rest-auth/', include('rest_auth.urls')),
]