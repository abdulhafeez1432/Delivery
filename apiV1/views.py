from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from app.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsCustomerUser, IsOwner
from app.models import *
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from rest_framework.viewsets import ModelViewSet

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })





class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user





class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ProfileCustomer.objects.all()
    serializer_class = ProfileCustomerSerializer
    permission_classes = (IsOwner,)

    # Ensure a user sees only own The Profile.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ProfileCustomer.objects.filter(user=user)
        raise PermissionDenied()
        
 
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        #email send_email


class CategoryDetailsAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailsSerializer
    permission_classes = (IsAuthenticated,)


# class SubCategoryDetailsAPIView(generics.ListAPIView):
#     #queryset = SubCategory.objects.all()
#     serializer_class = CategoryDetailsSerializer
#     permission_classes = (IsAuthenticated,)


#      # Ensure a user sees only own The Profile.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return ProfileCustomer.objects.filter(user=user)
#         raise PermissionDenied()




class PalceOrder(APIView):
    serializer_class = ProcessOrderSerializer

            

    def get(self, request, category_pk, format=None):
        category = get_object_or_404(Category, pk=category_pk)
        subcategory = category.subcategory.all()
        

        data = {'subcategory': subcategory, 'category_pk': category_pk,}
        serializer = PlaceOrderSerializer(data, many=True)
        if category:
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
    def post(self, request, category_pk):
        category_pk = request.data.get("category")
        data = {'category_pk': category_pk}
        serializer = PlaceOrderSerializer(data=data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SubCategoryDetailsAPIView(generics.ListAPIView):
#     #queryset = SubCategory.objects.all()
#     serializer_class = CategoryDetailsSerializer
#     permission_classes = (IsAuthenticated,)


#      # Ensure a user sees only own The Profile.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return ProfileCustomer.objects.filter(user=user)
#         raise PermissionDenied()




class SubCategoryCategoryDetailsAPIView(generics.ListCreateAPIView):
        
    serializer_class = OrderSubCategorySerializer
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return SubCategory.objects.filter(category=category.id)



class ProcessItemAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSubCategorySerializer
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return SubCategory.objects.filter(category=category.id)







#class ProcessFoodCreate(generics.CreateAPIView):



# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     # Add this code block
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'create':
#             permission_classes = [AllowAny]
#         elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsLoggedInUserOrAdmin]
#         elif self.action == 'list' or self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]
